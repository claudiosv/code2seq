#!/bin/bash

config=configs/java-small-high-maxparts.json
model=vsc/models/java-small-case-10k
model_iter=8
dataset=java-small-case-10k
python3 code2seq.py --config ${config} --load models/${model}/model_iter${model_iter} --test data/${dataset}/${dataset}.test.c2s

model=vsc/models/java-small-case-1k
model_iter=11
dataset=java-small-case-1k
# python3 code2seq.py --config ${config} --load models/${model}/model_iter${model_iter} --test data/${dataset}/${dataset}.test.c2s