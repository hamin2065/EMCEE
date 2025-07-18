#!/bin/bash

export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"

# Set common variables
DATASET_NAME=$1    # Options: M3Exam, MKQA, XNLI, XCOPA
MODEL=$2           # Options: gpt, claude, llama

# If using emulsify, set the required ENG_COT_PATH
ENG_COT_PATH="${DATASET_NAME}/${MODEL}/en-cot/"

# Define the strategies you want to run
STRATEGIES=("native-basic" "en-basic" "native-cot" "en-cot" "XLT") #--> baselines
# STRATEGIES=("extract" "emulsify") #--> EmCei

# Define dataset-specific language symbols
if [ "$DATASET_NAME" == "M3Exam" ]; then
    symbols="af it jv pt sw th vi zh"
elif [ "$DATASET_NAME" == "XCOPA" ]; then
    symbols="et ht id it qu sw ta th tr vi zh"
elif [ "$DATASET_NAME" == "MKQA" ]; then
    symbols="de es fr ja ru th tr vi zh_cn"
elif [ "$DATASET_NAME" == "XNLI" ]; then
    symbols="ar bg de el es fr hi ru sw th tr ur vi zh"
else
    echo "ERROR: Unknown dataset name: $DATASET_NAME"
    exit 1
fi


for STRATEGY in "${STRATEGIES[@]}"; do
    
    for DATA_SYMBOL in $symbols; do
        
        DATASET_PATH="./data/${DATASET_NAME}/${DATA_SYMBOL}-test.json"

        # If the strategy is en-based, we override the evaluation language to 'en'
        if [[ "$STRATEGY" == "en-basic" || "$STRATEGY" == "en-cot"|| "$STRATEGY" == "XLT" || "$STRATEGY" == "extract" || "$STRATEGY" == "emulsify" ]]; then
            EVAL_SYMBOL="en"
        else
            EVAL_SYMBOL="$DATA_SYMBOL"
        fi

        echo "---------------------------------------"
        echo "Running Strategy:    $STRATEGY"
        echo "Using Dataset File:  $DATASET_PATH"
        echo "Data Language:       $DATA_SYMBOL"
        echo "Eval Language:       $EVAL_SYMBOL"
        echo "---------------------------------------"

        CMD="python3 main.py \
            --dataset_path ${DATASET_PATH} \
            --dataset_name ${DATASET_NAME} \
            --model ${MODEL} \
            --strategy ${STRATEGY} \
            --data_symbol ${DATA_SYMBOL} \
            --eval_symbol ${EVAL_SYMBOL}"

        if [ "$STRATEGY" == "emulsify" ]; then
           CMD+=" --eng_cot_path ./results/${DATASET_NAME}/${MODEL}/en-cot/${DATA_SYMBOL}-test.json"
           CMD+=" --extract_path ./results/${DATASET_NAME}/${MODEL}/extract/${DATA_SYMBOL}-test.json"
        fi

        echo "Running command: $CMD"
        eval "$CMD"
    done
done