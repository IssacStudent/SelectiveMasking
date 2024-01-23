source data/create_data_rule/config.sh
SHARD_COUNT=0
rm xarg_list.txt
touch xarg_list.txt
PART=0
for GPU_ID in ${GPU_LIST[@]}; do
  echo "${GPU_ID} ${PART}">> xarg_list.txt
  ((PART++))
done
chmod 777 data/create_data_rule/create_mask_dataset.sh
xargs -n 2 --max-procs=${MAX_PROC}  --arg-file=xarg_list.txt data/create_data_rule/create_mask_dataset.sh
rm xarg_list.txt

#--input_dir=data/datasets/absa/laptop/ --output_dir=data/datasets/test/full_rule_mask/ --max_seq_length=128 --max_predictions_per_seq=20 --masked_lm_prob=0.15 --random_seed=12345 --dupe_factor=1 --bert_model=results/test/origin/CKPT_1M/42/best_model/ --task_name=absa_term --top_sen_rate=1 --part 0 --threshold=0.01 --max_proc=2 --mode=rule --do_lower_case
#--input_dir=data/datasets/absa/laptop/ --output_dir=data/datasets/test/full_rule_mask/ --max_seq_length=128 --max_predictions_per_seq=20 --masked_lm_prob=0.15 --random_seed=12345 --dupe_factor=1 --bert_model=results/test/origin/CKPT_1M/42/best_model/ --task_name=absa_term --top_sen_rate=1 --part 1 --threshold=0.01 --max_proc=2 --mode=rule --do_lower_case
