#!/bin/bash

TRAIN_DIR=java-small/training
VAL_DIR=java-small/validation
TEST_DIR=java-small/test
DATASET_NAME=java-small
BPE_DATASET_NAME=java-small-nocase-10k-split
MAX_DATA_CONTEXTS=1000
MAX_CONTEXTS=200 #the number of sampled paths from each example (which we set to 200 in the final models).
SUBTOKEN_VOCAB_SIZE=186277
TARGET_VOCAB_SIZE=26347
NUM_THREADS=16
PYTHON=python3
APPLY_BPE=true
BPE_MERGES=/home/students/cspiess/dataprep/dataprep/data/bpe/nocase/10k/merges.txt
###########################################################

TRAIN_DATA_FILE=/data/cspiess/java-small/${DATASET_NAME}.train.c2s
VAL_DATA_FILE=/data/cspiess/java-small/${DATASET_NAME}.val.c2s
TEST_DATA_FILE=/data/cspiess/java-small/${DATASET_NAME}.test.c2s

BPE_TRAIN_DATA_FILE=/data/cspiess/${BPE_DATASET_NAME}/${BPE_DATASET_NAME}.train.raw.txt
BPE_VAL_DATA_FILE=/data/cspiess/${BPE_DATASET_NAME}/${BPE_DATASET_NAME}.val.raw.txt
BPE_TEST_DATA_FILE=/data/cspiess/${BPE_DATASET_NAME}/${BPE_DATASET_NAME}.test.raw.txt

TRAIN_DATA_FILE=${BPE_TRAIN_DATA_FILE}
VAL_DATA_FILE=${BPE_VAL_DATA_FILE}
TEST_DATA_FILE=${BPE_TEST_DATA_FILE}

TARGET_HISTOGRAM_FILE=data/cspiess/${BPE_DATASET_NAME}/${BPE_DATASET_NAME}.histo.tgt.c2s
SOURCE_SUBTOKEN_HISTOGRAM=data/cspiess/${BPE_DATASET_NAME}/${BPE_DATASET_NAME}.histo.ori.c2s
NODE_HISTOGRAM_FILE=data/cspiess/${BPE_DATASET_NAME}/${BPE_DATASET_NAME}.histo.node.c2s

echo "Creating histograms from the training data"
cat ${TRAIN_DATA_FILE} | cut -d' ' -f1 | tr '|' '\n' | awk '{n[$0]++} END {for (i in n) print i,n[i]}' >${TARGET_HISTOGRAM_FILE}
cat ${TRAIN_DATA_FILE} | cut -d' ' -f2- | tr ' ' '\n' | cut -d',' -f1,3 | tr ',|' '\n' | awk '{n[$0]++} END {for (i in n) print i,n[i]}' >${SOURCE_SUBTOKEN_HISTOGRAM}
cat ${TRAIN_DATA_FILE} | cut -d' ' -f2- | tr ' ' '\n' | cut -d',' -f2 | tr '|' '\n' | awk '{n[$0]++} END {for (i in n) print i,n[i]}' >${NODE_HISTOGRAM_FILE}

${PYTHON} preprocess.py --train_data ${TRAIN_DATA_FILE} --test_data ${TEST_DATA_FILE} --val_data ${VAL_DATA_FILE} \
  --max_contexts ${MAX_CONTEXTS} --max_data_contexts ${MAX_DATA_CONTEXTS} --subtoken_vocab_size ${SUBTOKEN_VOCAB_SIZE} \
  --target_vocab_size ${TARGET_VOCAB_SIZE} --subtoken_histogram ${SOURCE_SUBTOKEN_HISTOGRAM} \
  --node_histogram ${NODE_HISTOGRAM_FILE} --target_histogram ${TARGET_HISTOGRAM_FILE} --output_name /data/cspiess/${BPE_DATASET_NAME}/${BPE_DATASET_NAME}
