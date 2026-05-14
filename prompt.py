from typing import Dict
from multilingual import dataset_lang_mapping

class PromptingStrategy:
    """Defines multilingual prompting strategies for various tasks."""

    dataset_mapping = {
        "M3Exam": {
            "task_type": "a multiple-choice answering",
            "answer_type": "obtain an option",
            "answer_format": "'Answer: [option]'"
        },
        "MKQA": {
            "task_type": "an open-ended question answering",
            "answer_type": "provide a text answer",
            "answer_format": "'Answer: [response]'"
        },
        "XCOPA": {
            "task_type": "commonsense reasoning",
            "answer_type": "pick a choice",
            "answer_format": "'Choice number: [1 or 2]'"
        },
        "XNLI": {
            "task_type": "a natural language inference",
            "answer_type": "determine the entailment",
            "answer_format": "'Answer: [yes/no/maybe]'"
        }
    }

    @staticmethod
    def native_basic(data: Dict, language: str, dataset: str) -> str:
        """Native basic prompting in the given language."""
        base_prompt = dataset_lang_mapping[dataset]["base_prompt"].get(language, dataset_lang_mapping[dataset]["base_prompt"]["en"])
        # main_prompt = dataset_lang_mapping[dataset]["main_prompt"].get(language, dataset_lang_mapping[dataset]["main_prompt"]["en"])
        answer_prompt = dataset_lang_mapping[dataset]["answer_prompt"].get(language, dataset_lang_mapping[dataset]["answer_prompt"]["en"])
    
        if dataset == "M3Exam":
            if "question" in data and "options" in data:
                options_text = "\n".join(data['options'])
                return f"{base_prompt}\n{data['question']}\n{options_text}\n{answer_prompt}"
        
        elif dataset == "MKQA":
            if "query" in data:
                if data["answer"][0]['type'] == "binary":  # for binary questions, answer should be either 'yes' or 'no'
                    binary_prompt = dataset_lang_mapping[dataset]["binary_prompt"].get(language, dataset_lang_mapping[dataset]["base_prompt"]["en"])
                    return f"{base_prompt}\n{data['query']}\n{binary_prompt}\n{answer_prompt}"
                return f"{base_prompt}\n{data['query']}\n{answer_prompt}"

        elif dataset == "XNLI":
            if "premise" in data and "hypothesis" in data:
                return f"{base_prompt}\nPremise: {data['premise']}\nHypothesis: {data['hypothesis']}\n{answer_prompt}"

        elif dataset == "XCOPA":
            
            if data['question'] == "effect": # question is either 'effect' or 'cause'
                question  = dataset_lang_mapping[dataset]["main_prompt"].get(language, dataset_lang_mapping[dataset]["main_prompt"]["en"])['effect']
            else: 
                question = dataset_lang_mapping[dataset]["main_prompt"].get(language, dataset_lang_mapping[dataset]["main_prompt"]["en"])['cause']

            base_prompt = base_prompt.replace(
                '[premise]', data['premise']
            ).replace(
                '[question]', question
            ).replace(
                '[choice1]', data['choice1']
            ).replace(
                '[choice2]', data['choice2']
            )
            return f"{base_prompt}\n{answer_prompt}"

        return "Unknown format."

    @staticmethod
    def en_basic(data: Dict, dataset: str) -> str:
        """English basic prompting (translated from the native language)."""
        return PromptingStrategy.native_basic(data, "en", dataset)

    @staticmethod
    def native_cot(data: Dict, language: str, dataset: str) -> str:
        """Native Chain-of-Thought (CoT) prompting."""

        base_prompt = dataset_lang_mapping[dataset]["base_prompt"].get(language, dataset_lang_mapping[dataset]["base_prompt"]["en"])
        cot_text = dataset_lang_mapping[dataset]["cot_prompt"].get(language, dataset_lang_mapping[dataset]["cot_prompt"]["en"])
        # main_prompt = dataset_lang_mapping[dataset]["main_prompt"].get(language, dataset_lang_mapping[dataset]["main_prompt"]["en"])
        answer_prompt = dataset_lang_mapping[dataset]["answer_prompt"].get(language, dataset_lang_mapping[dataset]["answer_prompt"]["en"])
    
        # **Dataset-Specific Formatting**
        if dataset == "M3Exam":
            if "question" in data and "options" in data:
                # options_text = "\n".join([f"{chr(65 + i)}. {opt}" for i, opt in enumerate(data["options"])])
                options_text = "\n".join(data['options'])
                return f"{base_prompt}\n{data['question']}\n{options_text}\n{cot_text}\n{answer_prompt}"
        
        elif dataset == "MKQA":
            if "query" in data:
                if data["answer"][0]['type'] == "binary":  # for binary questions, answer should be either 'yes' or 'no'
                    binary_prompt = dataset_lang_mapping[dataset]["binary_prompt"].get(language, dataset_lang_mapping[dataset]["base_prompt"]["en"])
                    return f"{base_prompt}\n{data['query']}\n{binary_prompt}\n{cot_text}\n{answer_prompt}"
                return f"{base_prompt}\n{data['query']}\n{cot_text}\n{answer_prompt}"

        elif dataset == "XNLI":
            if "premise" in data and "hypothesis" in data:
                return f"{base_prompt}\nPremise: {data['premise']}\nHypothesis: {data['hypothesis']}\n{cot_text}\n{answer_prompt}"

        elif dataset == "XCOPA":
            
            if data['question'] == "effect": # question is either 'effect' or 'cause'
                question  = dataset_lang_mapping[dataset]["main_prompt"].get(language, dataset_lang_mapping[dataset]["main_prompt"]["en"])['effect']
            else: 
                question = dataset_lang_mapping[dataset]["main_prompt"].get(language, dataset_lang_mapping[dataset]["main_prompt"]["en"])['cause']

            base_prompt = base_prompt.replace(
                '[premise]', data['premise']
            ).replace(
                '[question]', question
            ).replace(
                '[choice1]', data['choice1']
            ).replace(
                '[choice2]', data['choice2']
            )
            return f"{base_prompt}\n{cot_text}\n{answer_prompt}"

        return "Unknown format."

    @staticmethod
    def en_cot(data: Dict, dataset: str) -> str:
        """English Chain-of-Thought (CoT) prompting."""
        return PromptingStrategy.native_cot(data, "en", dataset)

    @staticmethod
    def xlt(data: Dict, symbol: str, dataset: str) -> str:

        language = dataset_lang_mapping.get(dataset, {}).get("lang_by_symbol", {}).get(symbol, "Unknown Language")
        dataset_obj = PromptingStrategy.dataset_mapping.get(dataset, {})
        
        if not dataset_obj:
            raise ValueError(f"Invalid dataset: {dataset}")

        # request = data.get("request", "[Missing request]")
        user_prompt = ""
        if dataset == 'M3Exam': 
            options_string = "\n".join(data['options'])
            user_prompt += f"I want you to act as a question answering expert for {language}.\n"
            user_prompt += f"Request: {data['question']}\n"
            user_prompt += f"{options_string}\n"
            user_prompt += f"You should retell the request in English.\n"
            user_prompt += f"You should step-by-step answer to obtain an option.\n"
            user_prompt += f"You should tell me the answer in this format: 'Answer: [option]'."

        elif dataset == "MKQA": 
            user_prompt += f"I want you to act as a question answering expert for {language}.\n"
            user_prompt += f"Question: {data['query']}\n"
            user_prompt += f"You should retell the question in English.\n"
            user_prompt += f"You should answer the question in English in one or a few words.\n"
            user_prompt += f"You should step-by-step answer the request.\n"
            user_prompt += f"You should tell me the answer in one or a few words in English in this format 'Answer: '\n"

            if data['answer'][0]['type'] == 'binary': 
                user_prompt += "Answer should be either 'yes' or 'no'."
        
        elif dataset == "XNLI": 
            user_prompt += f"I want you to act as a natural language inference expert for {language}.\n"
            user_prompt += f"Premise: {data['premise']}\n"
            user_prompt += f"Hypothesis: {data['hypothesis']}\n"
            user_prompt += f"You should retell the premise and hypothesis in English.\n"
            user_prompt += f"You should judge whether the hypothesis is true (entailment), false (contradiction), or undetermined (neutral) given the premise. The relationship can be chosen from entailment, contradiction, and neutral.\n"
            user_prompt += f"You should step-by-step answer the request.\n"
            user_prompt += f"You should tell me the relationship in this format 'Relationship: [entailment/contradiction/neutral]'.\n"

        elif dataset == "XCOPA": 
            user_prompt += f"I want you to act as a commonsense reasoning expert for {language}.\n"
            user_prompt += f"Here is a premise: {data['premise']}. What is the {data['question']}? Help me pick the more plausible option: -choice1: {data['choice1']}, -choice2: {data['choice2']}.\n"
            user_prompt += f"You should retell the premise and the options in English.\n"
            user_prompt += f"You should do step-by-step answer to pick a choice.\n"
            user_prompt += f"You should step-by-step answer the request.\n"
            user_prompt += f"You should tell me the choice number in this format 'Answer: '.\n"

        else: 
            raise ValueError(f"Invalid dataset: {dataset}")
        
        return user_prompt

    @staticmethod
    def get_prompt(strategy: str, data: Dict, dataset_name: str, target_lang="en") -> str:
        """
        Selects the correct prompting strategy based on the dataset and language.
        
        :param strategy: One of ('native-basic', 'en-basic', 'native-cot', 'en-cot', 'XLT')
        :param data: The dataset sample (question, premise, etc.)
        :param file_path: The dataset file path (used to extract language info)
        :param dataset: The dataset name (M3Exam, MKQA, XCOPA, XNLI)
        :param target_lang: The target language for XLT (default: English)
        :return: Formatted prompt string
        """
        # Extract the language from the filename (assumes 'xx-' prefix in filename)
        # symbol = file_path.split('/')[-1].split('-')[0]
        symbol = target_lang
        # detected_language = dataset_lang_mapping[dataset]["lang_by_symbol"].get(language_symbol, "en")
        # print(symbol)
        # print(dataset_name)
        strategy_methods = {
            "native-basic": lambda: PromptingStrategy.native_basic(data, symbol, dataset_name),
            "en-basic": lambda: PromptingStrategy.en_basic(data, dataset_name),
            "native-cot": lambda: PromptingStrategy.native_cot(data, symbol, dataset_name),
            "en-cot": lambda: PromptingStrategy.en_cot(data, dataset_name),
            "XLT": lambda: PromptingStrategy.xlt(data, symbol, dataset_name),
        }

        if strategy not in strategy_methods:
            raise ValueError(f"Invalid strategy '{strategy}'. Choose from {list(strategy_methods.keys())}")

        return strategy_methods[strategy]()

class EmceePrompting:
    XNLI_relation = {
        0: 'entailment',
        1: 'neutral',
        2: 'contradiction'
    }

    '''
    few-shot learning
    
    '''
    @staticmethod
    def extracting_generate(data: Dict, symbol: str, dataset: str) -> str:
        language = dataset_lang_mapping[dataset]['lang_by_symbol'][symbol]
        if dataset == "M3Exam": 
            system_prompt = f"I have written a multiple-choice question in {language.capitalize()}, along with the options. Your task is to write a short explanation (3-5 sentences) in English that helps students choose the correct answer. The explanation should, if necessary, include cultural or contextual elements related to the question to improve understanding. It should highlight important concepts or reasoning to help students make the choice."
            # if isinstance(data['options'], list):
            #     user_prompt = f"{data['question']}\n{"\n".join(data['options'])}"
            # elif isinstance(data['options'], str):
            #     user_prompt = f"{data['question']}\n{data['options']}"
            options = "\n".join(data['options']) if isinstance(data['options'], list) else data['options']
            user_prompt = f"{data['question']}\n{options}"

        elif dataset == "XNLI": 
            system_prompt = f"I have a premise and hypothesis in {language.capitalize()} for natural language inference task. My task goal is to judge whether the hypothesis is true, false, or undetermined given the premise. The relationship can be chosen from entailment, contradiction, and neutral.  Your task is to write a short explanation (3-5 sentences) in English that helps students get the correct answer. The explanation should, if necessary, include cultural or contextual elements related to the question to improve understanding. It should highlight important concepts or reasoning to help students generate correct answer."
            user_prompt = f"Premise: {data['premise']}\nHypothesis: {data['hypothesis']}"
        
        elif dataset == 'MKQA': 
            system_prompt = f"I have a question in {language.capitalize()}. Your task is to write a short explanation (3-5 sentences) in English that helps students get the correct answer. The explanation should, if necessary, include cultural or contextual elements related to the question to improve understanding. It should highlight important concepts or reasoning to help students generate correct answer."
            user_prompt = f"{data['query']}"

        elif dataset == 'XCOPA':
            system_prompt = f"I have a premise, a question, and two choices in {language.capitalize()} for a common-sense reasoning task. Your task is to write a short explanation (3-5 sentences) in English that helps students choose the correct choice. The explanation should, if necessary, include cultural or contextual elements related to the question to improve understanding. It should highlight important concepts or reasoning to help students make the correct choice."
            user_prompt = f"Premise: {data['premise']}\nWhat is the {data['question']}?\nChoice1: {data['choice1']}\nChoice2: {data['choice2']}"

        return system_prompt, user_prompt 

    @staticmethod
    def extracting_qa(data: Dict, symbol: str, dataset: str, explanation: str) -> str:
        if dataset == "M3Exam":
            system_prompt = "The following is a multiple choice question. Given question, explanation and options, write only the correct option without any other details or explanations."
            options = "\n".join(data['options']) if isinstance(data['options'], list) else data['options']
            user_prompt = f"Question: {data['question']}\nOptions: {options}\nExplanation: {explanation}"
        elif dataset == "XNLI": 
            system_prompt = 'You are an expert in natural language inference tasks. Given the premise, hypothesis, and explanation, your task is to judge whether the hypothesis is an entailment, contradiction, or neutral with respect to the premise. Provide your answer in the format: "Relationship: [Entailment, Neutral, or Contradiction].'
            user_prompt = f"Premise: {data['premise']}\nHypothesis: {data['hypothesis']}\nExplanation: {explanation}"
        elif dataset == 'MKQA': 
            system_prompt = f'The following is a reasoning question. Given question and explanation, write answer with format of "Answer: [one or a few words]".'
            user_prompt = f"Question: {data['query']}\nExplanation: {explanation}"
            if data["answer"][0]['type'] == "binary":  # for binary questions, answer should be either 'yes' or 'no'
                user_prompt += 'Answer should be either "yes" or "no".'
        elif dataset == 'XCOPA':
            system_prompt = 'You are an expert in commonsense reasoning tasks. Given the premise, question, two options and explanation, your task is to pick the more plausible option. You should only choose one option for your answer. You should answer the question in format of "Answer: [1 or 2]"'
            user_prompt = f"Premise: {data['premise']}\nWhat is the {data['question']}?\nChoice1: {data['choice1']}\nChoice2: {data['choice2']}\nExplanation: {explanation}"
        return system_prompt, user_prompt
    
    # input: ENG-COT answer, EXTRACT answer
    def merging(data: Dict, eng_cot_data: Dict, extract_data: Dict, symbol: str, dataset: str) -> str:
        language = dataset_lang_mapping[dataset]['lang_by_symbol'][symbol]
        extract_data_answer = extract_data['explanation'] + "\nAnswer: " + extract_data['response']
        eng_cot_answer = eng_cot_data['response']
        en_prompt = "Your response should be in English."
        if dataset == "M3Exam":
            sys_prompt = f'''You are a judge from the {language.capitalize()} tradition, known for your wisdom and fairness. Although your cultural background is {language.capitalize()}, you are fluent in English and will conduct this task in English. You are given a Question and its corresponding Options. There is a debate on this question between user1 and user2. Your task is to listen to their arguments carefully and provide a fair and wise judgment.
{en_prompt}
Summarize the debate briefly and then give a conclusion based on the arguments presented. Your response should be in the format: 
"Summary: ___. Conclusion: [option] is more plausible.

Answer: [option]"

Approach the task with the fairness and critical thinking expected of a {language.capitalize()} judge, ensuring you choose only one option for the final answer.'''
            options_string = "\n".join(data['options'])
            user_prompt = f"Question: {data['question']}\nOptions: {options_string}\n\nuser1: {eng_cot_answer}\n\nuser2: {extract_data_answer}"

        elif dataset == "MKQA": 
            sys_prompt = f'''You are a judge from the {language.capitalize()} tradition, known for your wisdom and fairness. Although your cultural background is {language.capitalize()}, you are fluent in English and will conduct this task in English. You are given a reasoning question. There is a debate on this question between user1 and user2. Your task is to listen to their arguments carefully and provide a fair and wise judgment.
{en_prompt}
Summarize the debate briefly and then give a conclusion based on the arguments presented. Your response should be in the format: 
"Summary: ___. Conclusion: [answer] is more plausible.

Answer: [one or a few words in English]"

Approach the task with the fairness and critical thinking expected of a {language.capitalize()} judge, ensuring you make only one answer for the final answer.'''

            user_prompt = f"Question: {data['query']}\n\nuser1: {eng_cot_answer}\n\nuser2: {extract_data_answer}"

        elif dataset == "XNLI": 
            sys_prompt = f'''You are a judge from the {language.capitalize()} tradition, known for your wisdom and fairness. Although your cultural background is {language.capitalize()}, you are fluent in English and will conduct this task in English. You are given a premise and a premise along with hypothesis. There is a debate on this question between user1 and user2. Your task is to listen to their arguments carefully and provide a fair and wise judgment.
{en_prompt}
Summarize the debate briefly and then give a conclusion based on the arguments presented. Your response should be in the format: 
"Summary: ___.
Conclusion: [entailment, neutral or contradiction] is more reasonable or contextually accurate.

Relationship: [entailment, neutral or contradiction]"

Approach the task with the fairness and critical thinking expected of a {language.capitalize()} judge, ensuring you make only one answer for the final answer.'''
            
            user_prompt = f"Premise: {data['premise']}\nHypothesis: {data['hypothesis']}\n\nuser1: {eng_cot_answer}\n\nuser2: {extract_data_answer}"
        elif dataset == "XCOPA": 
            sys_prompt = f'''You are a judge from the {language.capitalize()} tradition, known for your wisdom and fairness. You are given a qualitative or interpretive premise, question and two options. A debate between user1 and user2 follows, where each presents logical reasoning or factual evidence to support their answer. 
{en_prompt}
Task:
Summarize the key points and reasoning presented by both sides.
Conclude which option is more scientifically or mathematically accurate based on the debate.

Response Format:
Summary: [Concise summary of the debate and reasoning presented].
Conclusion: [Choice1 or Choice2] is more scientifically/mathematically accurate.

Answer: [1 or 2]'''

            user_prompt = f"Premise: {data['premise']}\nWhat is the {data['question']}?\nChoice1: {data['choice1']}\nChoice2: {data['choice2']}\n\nuser1: {eng_cot_answer}\n\nuser2: {extract_data_answer}"

        return sys_prompt, user_prompt

    @staticmethod
    def get_answer_prompt(data: Dict, dataset: str) -> str:
        if dataset == "M3Exam":
            return data['ground_truth']
        elif dataset == "XNLI": 
            return EmceePrompting.XNLI_relation[data['label']]
        elif dataset == 'MKQA': 
            return data['answer'][0]['text']
        elif dataset == 'XCOPA':
            return data['label']
        else:
            raise ValueError(f"Invalid dataset '{dataset}'")