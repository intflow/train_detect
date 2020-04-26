#!/bin/bash

# Exit script on error.
set -e
# Echo each command, easier for debugging.
set -x


source "$PWD/constants.sh"

NUM_TRAINING_STEPS=50000 && \
NUM_EVAL_STEPS=2000

mkdir -p "${TRAIN_DIR}"

cd "$TF_BASE"
python object_detection/model_main.py \
  --pipeline_config_path="${CKPT_DIR}/pipeline.config" \
  --model_dir="${TRAIN_DIR}" \
  --num_train_steps="${NUM_TRAINING_STEPS}" \
  --num_eval_steps="${NUM_EVAL_STEPS}"
