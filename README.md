# EMCEI
**E**xtracting and e**m**ulsifying **c**ultural **e**xplanat**i**ons(EMCEI)

This repository contains the codebase for EMCEI, a two-step approach that enhances the multilingual performance of large language models (LLMs) by:

1. Extracting cultural context from the model's parametric knowledge, and

2. Emulsifying it using an LLM-as-Judge to select responses that effectively balance cultural relevance with reasoning ability.

[📄 EMCEI Paper on arXiv](https://arxiv.org/abs/2503.05846)


# Requirements
```sh
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
```
Install dependencies: 
```py
pip install -r requirements.txt
```
This project was tested using `Python 3.12`
# Datasets
All datasets used in this project can be found in the `./data` directory.


# Usage
Run evaluation using: 
```sh
./run_evaluation.sh {dataset} {model} {strategy}
```
Example: 
```sh
./run_evaluation.sh M3Exam gpt en-cot
```
- Dataset options: `M3Exam`, `MKQA`, `XNLI`, `XCOPA`
- Model options: `gpt`, `claude`, `llama`
- Strategy options
    - Baseline options: `native-basic`, `native-cot`, `en-basic`, `en-cot`, `XLT`
    - Main experiment options: `extract`, `emulsify`
---
**MKQA evaluation**

The MKQA evaluation component in this repository is based on the official MKQA repository: 
🔗 https://github.com/apple/ml-mkqa


