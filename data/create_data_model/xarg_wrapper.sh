source data/create_data_model/config.sh

SHARD_COUNT=0
rm xarg_list.txt
touch xarg_list.txt
PART=0
for GPU_ID in ${GPU_LIST[@]}; do
  echo "${GPU_ID} ${PART}">> xarg_list.txt
  ((PART++))
done
chmod 777 data/create_data_model/create_mask_dataset.sh
xargs -n 2 --max-procs=${MAX_PROC} --arg-file=xarg_list.txt data/create_data_model/create_mask_dataset.sh
rm xarg_list.txt

#--input_dir=data/datasets/amazon/ --output_dir=data/datasets/test/full_yelp/ --max_seq_length=256 --max_predictions_per_seq=40 --masked_lm_prob=0.15 --random_seed=12345 --dupe_factor=1 --bert_model=results/test/full_mask_generator/best_model/ --task_name=amazon --top_sen_rate=1 --part 0 --threshold=0.01 --max_proc=2 --mode=model --do_lower_case --with_rand
#--input_dir=data/datasets/amazon/ --output_dir=data/datasets/test/full_yelp/ --max_seq_length=256 --max_predictions_per_seq=40 --masked_lm_prob=0.15 --random_seed=12345 --dupe_factor=1 --bert_model=results/test/full_mask_generator/best_model/ --task_name=amazon --top_sen_rate=1 --part 1 --threshold=0.01 --max_proc=2 --mode=model --do_lower_case --with_rand