# coding=utf-8
from __future__ import print_function
import argparse
import torch
import time
import pickle
import os
import sys
sys.path.append("..")
from torch.autograd import Variable
from tqdm import tqdm
from global_utils import item_detail, result_diff, mask_result
from loader import *
from utils import *


t = time.time()

# python -m visdom.server

parser = argparse.ArgumentParser()
parser.add_argument(
    "-t", "--test", default="dataset/eng.testb",
    help="Test set location"
)
parser.add_argument(
    '--score', default='evaluation/temp/score.txt',
    help='score file location'
)
parser.add_argument(
    "-f", "--crf", action='store_true',
    help="Use CRF (0 to disable)"
)
parser.add_argument(
    "-g", '--use_gpu', action='store_true',
    help='whether or not to ues gpu'
)
parser.add_argument(
    '--loss', default='loss.txt',
    help='loss file location'
)
parser.add_argument(
    '--model_path', default='models/lstm_crf.model',
    help='model path'
)
parser.add_argument(
    '--map_path', default='models/mapping.pkl',
    help='model path'
)
parser.add_argument(
    '--char_mode', choices=['CNN', 'LSTM'], default='CNN',
    help='char_CNN or char_LSTM'
)
parser.add_argument(
    '--mask_rate', default=0, type=float,
    help='random mask data rate'
)
parser.add_argument(
    '--mask_num', default=0, type=int,
    help='random mask data number'
)
parser.add_argument(
    '--mask_samp', default=1, type=int,
    help="random mask sample number"
)
parser.add_argument(
    '--display_detail', action='store_true',
    help='wether display detail of mask'
)

args = parser.parse_args()

mapping_file = args.map_path

with open(mapping_file, 'rb') as f:
    mappings = pickle.load(f)

word_to_id = mappings['word_to_id']
tag_to_id = mappings['tag_to_id']
id_to_tag = {k[1]: k[0] for k in tag_to_id.items()}
char_to_id = mappings['char_to_id']
config = mappings['args']
word_embeds = mappings['word_embeds']

# use_gpu = args.use_gpu == 1 and torch.cuda.is_available()


assert os.path.isfile(args.test)
assert config.tag_scheme in ['iob', 'iobes']

if not os.path.isfile(eval_script):
    raise Exception('CoNLL evaluation script not found at "%s"' % eval_script)
if not os.path.exists(eval_temp):
    os.makedirs(eval_temp)

lower = config.lower
zeros = config.zeros
tag_scheme = config.tag_scheme
# mask_rate = parameters['mask_rate']

test_sentences = load_sentences(args.test, lower, zeros)
update_tag_scheme(test_sentences, tag_scheme)
test_data, all_masked_test_data = prepare_dataset(
    test_sentences, word_to_id, char_to_id, tag_to_id, lower, args.mask_num, args.mask_rate, args.mask_samp
)

model = torch.load(args.model_path)
model_name = args.model_path.split('/')[-1].split('.')[0]

if args.use_gpu:
    model.cuda()
model.eval()


def evaluate(model, datas, postfix=''):
    prediction = []
    confusion_matrix = torch.zeros((len(tag_to_id) - 2, len(tag_to_id) - 2))
    # print("OK")
    for data in datas:
        ground_truth_id = data['tags']
        words = data['str_words']
        chars2 = data['chars']
        caps = data['caps']

        if config.char_mode == 'LSTM':
            chars2_sorted = sorted(chars2, key=lambda p: len(p), reverse=True)
            d = {}
            for i, ci in enumerate(chars2):
                for j, cj in enumerate(chars2_sorted):
                    if ci == cj and not j in d and not i in d.values():
                        d[j] = i
                        continue
            chars2_length = [len(c) for c in chars2_sorted]
            char_maxl = max(chars2_length)
            chars2_mask = np.zeros(
                (len(chars2_sorted), char_maxl), dtype='int')
            for i, c in enumerate(chars2_sorted):
                chars2_mask[i, :chars2_length[i]] = c
            chars2_mask = Variable(torch.LongTensor(chars2_mask))

        if config.char_mode == 'CNN':
            d = {}
            chars2_length = [len(c) for c in chars2]
            char_maxl = max(chars2_length)
            chars2_mask = np.zeros(
                (len(chars2_length), char_maxl), dtype='int')
            for i, c in enumerate(chars2):
                chars2_mask[i, :chars2_length[i]] = c
            chars2_mask = Variable(torch.LongTensor(chars2_mask))

        dwords = torch.LongTensor(data['words'])
        dcaps = torch.LongTensor(caps)
        if args.use_gpu:
            val, out = model(dwords.cuda(), chars2_mask.cuda(),
                             dcaps.cuda(), chars2_length, d)
        else:
            val, out = model(dwords, chars2_mask, dcaps, chars2_length, d)
        predicted_id = out
        temp_pred = []
        for (word, true_id, pred_id) in zip(words, ground_truth_id, predicted_id):
            # line = ' '.join([word, id_to_tag[true_id], id_to_tag[pred_id]])
            # prediction.append(line)
            temp_pred.append([word, id_to_tag[true_id], id_to_tag[pred_id]])
            confusion_matrix[true_id, pred_id] += 1
        prediction.append(temp_pred)
    predf = eval_temp + '/pred.' + model_name + '_' + postfix
    scoref = eval_temp + '/score.' + model_name + '_' + postfix
    # print(predf)
    with open(predf, 'w') as f:
        for sen in prediction:
            for word in sen:
                f.write(' '.join(word) + '\n')
            f.write('\n')
        # f.write('\n'.join(prediction))

    os.system('%s < %s > %s' % (eval_script, predf, scoref))
    return prediction

    # with open(scoref, 'rb') as f:
    #     for l in f.readlines():
    #         print(l.strip())

    # print(("{: >2}{: >7}{: >7}%s{: >9}" % ("{: >7}" * confusion_matrix.size(0))).format(
    #     "ID", "NE", "Total",
    #     *([id_to_tag[i] for i in range(confusion_matrix.size(0))] + ["Percent"])
    # ))
    # for i in range(confusion_matrix.size(0)):
    #     print(("{: >2}{: >7}{: >7}%s{: >9}" % ("{: >7}" * confusion_matrix.size(0))).format(
    #         str(i), id_to_tag[i], str(confusion_matrix[i].sum()),
    #         *([confusion_matrix[i][j] for j in range(confusion_matrix.size(0))] +
    #           ["%.3f" % (confusion_matrix[i][i] * 100. / max(1, confusion_matrix[i].sum()))])
    #     ))


param = {"origin_param": {}, "mask_param": {
    "postfix": str(args.mask_rate) + '_' + str(args.mask_num)}}

mask_result(args.mask_samp, args.mask_num, args.mask_rate,
            args.display_detail, evaluate, model, test_data, all_masked_test_data, param)


print("Evaluation time: {}".format(time.time() - t))