#!/bin/bash

# Exit script on error.
set -e
# Echo each command, easier for debugging.
set -x


ckpt_number=0
source "$PWD/constants.sh"

#mkdir "${OUTPUT_DIR}"

echo "GENERATING label file..."
echo "0 pig_s" >> "${OUTPUT_DIR}/labels.txt"
echo "1 pig_l" >> "${OUTPUT_DIR}/labels.txt"

cd $TF_BASE
echo "EXPORTING frozen graph from checkpoint..."
python object_detection/export_tflite_ssd_graph.py \
  --pipeline_config_path="${CKPT_DIR}/pipeline.config" \
  --trained_checkpoint_prefix="${TRAIN_DIR}/model.ckpt-${ckpt_number}" \
  --output_directory="${OUTPUT_DIR}" \
  --add_postprocessing_op=true

echo "CONVERTING frozen graph to TF Lite file..."
tflite_convert \
  --output_file="${OUTPUT_DIR}/output_tflite_graph.tflite" \
  --graph_def_file="${OUTPUT_DIR}/tflite_graph.pb" \
  --inference_type=QUANTIZED_UINT8 \
  --input_arrays="${INPUT_TENSORS}" \
  --output_arrays="${OUTPUT_TENSORS}" \
  --mean_values=128 \
  --std_dev_values=128 \
  --input_shapes=1,300,300,3 \
  --change_concat_input_ranges=false \
  --allow_nudging_weights_to_use_fast_gemm_kernel=true \
  --allow_custom_ops

echo "TFLite graph generated at ${OUTPUT_DIR}/output_tflite_graph.tflite"
