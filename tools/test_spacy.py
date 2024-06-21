from transformers import AutoTokenizer, AutoModel
import torch
import json

def talk(input, history):

    return model.chat(tokenizer, input, history=history)
    # print("========================================================")
    # response, history = model.chat(tokenizer,
    #                                "请抽取下列句中三元组,以(头实体，关系，尾实体)的形式回答：审理查明：被告招募原告及许多新场乡农民到成都务工，2014年正月24日原告到成都后，被告安排原告到成都的各个建筑工地上务工。工作内容为：扫地、铲除混泥土块、砌墙、搬砖、背沙等杂活。",
    #                                history=history)
    # print(response)
    # print("========================================================")
    # response, history = model.chat(tokenizer,
    #                                "请抽取下列句中三元组,以(头实体，关系，尾实体)的形式回答：被告与原告口头约定：工钱按务工的天数计算，每天120元，加班另算；中途被告仅向原告预支生活费，年底结账。原告在被告处务工到2014年9月份左右。2015年8月24日被告向原告出具欠条一张，载明欠原告工资14020.00元，在2015年腊月30日前付清。",
    #                                history=history)
    # print(response)

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        datas = json.load(file)
        return datas

def save_json(file_path, datas):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(datas, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    torch.cuda.set_device(0)
    tokenizer = AutoTokenizer.from_pretrained("chatglm3-6b", trust_remote_code=True)
    model = AutoModel.from_pretrained("chatglm3-6b", trust_remote_code=True).half().cuda()
    model = model.eval()
    history = []
    # response, history = model.chat(tokenizer,
    #                             "你好，你是自然语言处理专家，先需要你使用自然语言抽取三元组,已知下列句子,请从句子中抽取出可能的(头实体,关系,尾实体)三元组,抽取实体类型为{'人类','组织','地理地区','物品','时间','合同','项目','法律','金额','数量','凭证','服务',''设施','事件'}等,关系类型为{'签订','签署','借款','期限','担保','抵押','欠款','记载','还款','付款','提供','委托','约定','判决','作出','导致','赊购','出具','支付','未支付','内容','具有','具备','质证','予以','为','生效'}等,你可以先识别出实体再判断三元组,以(头实体,关系,尾实体)的形式回答，头实体、关系和尾实体均为文中包含字词信息。句子在后续给出。",
    #                             history=history)
    # print(response
    print("==========================start==============================")
    i = 0
    datas = read_json("val_third_triple_1.json")
    length = len(datas)
    for data in datas:
        i += 1
        if i<200:
            continue
        print("====================总共" + str(length) + "条数据，当前处理到" + str(i) + "条数据====================")
        if i % 10 == 0:
            save_json("val_third_triple_1.json", datas)
            print(
                "++++++++++++++++++++++++++++++++断点保存成功！！！++++++++++++++++++++++++++++++++++++++")
        dealed = True
        subString = "关系"
        lentri = 0
        if "triples" in data:
            if "(头实体,关系,尾实体)" in data["triples"][0]:
                data["triples"].pop(0)
            for triple in data["triples"]:
                if len(triple.split(",")) == 2:
                    dealed = False
                    break
                if subString in triple:
                    lentri += 1
            if lentri == len(data["triples"]):
                dealed = False
            if len(data["triples"]) > 3 and len(data["triples"]) == len(set(data["triples"])) and dealed:
                print("已处理，跳过！")
                continue
        texts = []
        yuan = data['party'][0]
        defe = data['party'][1]
        text = ""
        if data["claim"]:
            claims = ""
            for claim in data["claim"]:
                claims = claims + claim
            response, history = talk(
                "你是自然语言处理专家，给定三元组模板为(头实体，关系，尾实体)，其中头实体与尾实体是名词，候选实体列表包括{" + yuan + "，" + defe + "，原告，被告}，关系尽量是动词且不要出现实体列表中的词语，请从下列给定文本中抽取出所有包含实体关系三元组。请严格按照至少五个(头实体，关系，尾实体)三段式格式呈现结果，不要输出不符合上述模板或格式的结果。文本为：" +
                claims, [])
            responses = response.split("\n")
            responses = list(set(responses))
            for text in responses:
                if len(text) > 0:
                    texts.append(text)
            print("claims处理完毕！")
            # text += ('claims' + claims)
        if data["defe"]:
            response, history = talk(
                "你是自然语言处理专家，给定三元组模板为(头实体，关系，尾实体)，其中头实体与尾实体是名词，候选实体列表包括{" + yuan + "，" + defe + "，原告，被告}，关系尽量是动词且不要出现实体列表中的词语，请从下列给定文本中抽取出所有包含实体关系三元组。请严格按照至少五个(头实体，关系，尾实体)三段式格式呈现结果，不要输出不符合上述模板或格式的结果。文本为：" +
                data["defe"], [])
            responses = response.split("\n")
            responses = list(set(responses))
            for text in responses:
                if len(text) > 0:
                    texts.append(text)
            print("defe处理完毕！")
        if data["plai"]:
            response, history = talk(
                "你是自然语言处理专家，给定三元组模板为(头实体，关系，尾实体)，其中头实体与尾实体是名词，候选实体列表包括{" + yuan + "，" + defe + "，原告，被告}，关系尽量是动词且不要出现实体列表中的词语，请从下列给定文本中抽取出所有包含实体关系三元组。请严格按照至少五个(头实体，关系，尾实体)三段式格式呈现结果，不要输出不符合上述模板或格式的结果。文本为：" +
                data["plai"], [])
            responses = response.split("\n")
            responses = list(set(responses))
            for text in responses:
                if len(text) > 0:
                    texts.append(text)
        texts.append("(" + yuan + ", 是, 原告" + ")")
        texts.append("(" + defe + ", 是, 被告" + ")")
        history = []
        data["triples"] = texts
        print(texts)
        print(
            "已处理完第" + str(i) + "条数据!")


    save_json("val_third_triple_1.json", datas)