#!/bin/bash

DATASET_NAME=java-small
BPE_DATASET_NAME=java-small-nocase-10k-split
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

mkdir -p /data/cspiess/${BPE_DATASET_NAME}

if [ "${APPLY_BPE}" = true ]; then
  echo "Preprocessing test dataset with BPE..."
  ${PYTHON} bpe.py -i ${TEST_DATA_FILE} -o ${BPE_TEST_DATA_FILE} -m ${BPE_MERGES} -p -lb
  echo "Finished encoding test dataset..."
fi