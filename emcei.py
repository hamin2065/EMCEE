import random, json
from dataset import Dataset
from models import GPTModel, ClaudeModel, LlamaModel
from evaluation import M3ExamEvaluator, MKQAEvaluator, XNLIEvaluator, XCOPAEvaluator
from prompt import EmCeiPrompting
from typing import List, Dict
import tqdm

# random.seed(42)

class EmCei:
    """EmCei evaluation on datasets with different prompting strategies."""

    def __init__(self, dataset_path: str, dataset_name: str, eng_cot_dataset_path: str, extraction_dataset_path: str, model_type: str, strategy: str, lang_symbol: str, data_symbol: str = "en"):
        """
        :param dataset_path: Path to the dataset file.
        :param model_type: Which model to use ('gpt', 'claude', 'llama').
        :param strategy: Prompting strategy ('native-basic', 'en-basic', 'native-cot', 'en-cot', 'XLT').
        :param data_symbol: Target language for XLT (default: English).
        """
        self.dataset = Dataset(dataset_path)
        self.dataset_name = dataset_name
        self.strategy = strategy
        self.lang_symbol = lang_symbol
        self.data_symbol = data_symbol
        self.data = self.dataset.load_data()
        self.model = self.load_model(model_type)
        self.eng_cot_dataset = Dataset(eng_cot_dataset_path)
        self.extract_dataset = Dataset(extraction_dataset_path)
        if strategy == 'emulsify': 
            self.eng_cot_data = self.eng_cot_dataset.load_data()
            self.extract_data = self.extract_dataset.load_data()
        self.evaluator = self.load_evaluator(dataset_name)


    def load_model(self, model_type: str):
        """Loads the selected model."""
        if model_type == "gpt":
            return GPTModel()
        elif model_type == "claude":
            return ClaudeModel()
        elif model_type == "llama":
            return LlamaModel()
        else:
            raise ValueError("Invalid model type. Choose from 'gpt', 'claude', 'llama'.")
        
    def load_evaluator(self, dataset_name: str):
        """Loads the correct evaluator based on dataset type."""
        if dataset_name == "M3Exam":
            return M3ExamEvaluator()
        elif dataset_name == "MKQA":
            return MKQAEvaluator()
        elif dataset_name == "XNLI":
            return XNLIEvaluator()
        elif dataset_name == "XCOPA":
            return XCOPAEvaluator()
        else:
            raise ValueError(f"Unknown dataset: {dataset_name}. No evaluator available.")

    def get_prompt(self, data: Dict) -> str:
        """Returns the formatted prompt based on the strategy and dataset type."""
        # dataset_name = self.dataset_name

        if self.strategy == 'extracting':
            return EmCeiPrompting.extract_run(self.strategy, data, self.dataset_name, self.data_symbol)
    
        elif self.strategy == 'emulsify': 
            return EmCeiPrompting.emulsify_run(self.strategy, data, self.dataset_name, self.data_symbol)

    def few_shot_exemplers_by_symbol(self, symbol): 
        """
        input: few shot path -> returns few-shot each dataset's few-shot-examples
        """
        with open(f"./few-shot/{self.dataset_name}.json", "r") as f:
            objs = json.load(f)

        if self.dataset_name == 'M3Exam': 
            num = 4 # max number of categories 
            cat_nums = len(objs[symbol].keys())
            num_for_one_category = num//cat_nums
            ls = []
            for cat_name, cat in objs[symbol].items():
                cat_value_sampled = random.sample(cat, num_for_one_category)
                for cat_value_sampled_i in cat_value_sampled:
                    cat_value_sampled_i['subject_category'] = cat_name
                    ls.append(cat_value_sampled_i)
            return ls

        elif self.dataset_name in ['MKQA', 'XNLI', 'XCOPA']:
            return objs[symbol].values()
        else: 
            raise ValueError()

    def make_few_shot_extract_gen_format(self, few_shot_examples):
        """
        make few-shot-examples in prompting format (generation)
        """
        
        few_shot_list = []

        for few_shot in few_shot_examples: 
            _, few_shot_user = EmCeiPrompting.extracting_generate(few_shot, self.data_symbol, dataset=self.dataset_name)
            few_shot_assist = few_shot['explanation']

            few_shot_list.append([few_shot_user, few_shot_assist])

        return few_shot_list
            
    def make_few_shot_extract_qa_format(self, few_shot_examples):
        """
        make few-shot-examples in prompting format (question-answering)
        """
        
        few_shot_list = []

        for few_shot in few_shot_examples: 
            _, few_shot_user = EmCeiPrompting.extracting_qa(few_shot, '', dataset=self.dataset_name, explanation=few_shot['explanation'])
            few_shot_assist = EmCeiPrompting.get_answer_prompt(few_shot, dataset=self.dataset_name)

            few_shot_list.append([few_shot_user, str(few_shot_assist)])

        return few_shot_list

    def extract_run(self):
        """Runs the baseline on a sample of data points."""

        results = []
        for idx, data_point in tqdm.tqdm(enumerate(self.data), total=len(self.data)):
            # generate explanation
            ex_sys_prompt, ex_user_prompt = EmCeiPrompting.extracting_generate(data_point, self.data_symbol, self.dataset_name)
            gen_few_shot_examples = self.few_shot_exemplers_by_symbol(self.data_symbol)
            gen_formatted_few_shot_examples = self.make_few_shot_extract_gen_format(gen_few_shot_examples)
            explanation_response = self.model.generate_response(ex_sys_prompt, ex_user_prompt, gen_formatted_few_shot_examples)
            # generate answer
            sys_prompt, user_prompt = EmCeiPrompting.extracting_qa(data_point, self.data_symbol, self.dataset_name, explanation_response)
            qa_few_shot_examples = self.few_shot_exemplers_by_symbol(self.data_symbol)
            qa_formatted_few_shot_examples = self.make_few_shot_extract_qa_format(qa_few_shot_examples)
            response = self.model.generate_response(sys_prompt, user_prompt, qa_formatted_few_shot_examples)
            predicted_answer = self.evaluator.extract_answers(response, 'en')
            if (self.dataset_name == 'MKQA') and (data_point['answer'][0]['type'] == 'binary'): 
                predicted_answer = self.evaluator.check_binary_answer(self.data_symbol, predicted_answer)
                is_correct = None
                ground_truth = data_point['answer']
            elif self.dataset_name == 'MKQA':
                is_correct = None
                ground_truth = data_point['answer']
            else: 
                ground_truth, is_correct = self.evaluator.check_answer(
                                                data_point, 
                                                predicted_answer,
                                                self.data_symbol
                                            )

            obj = {
                "id": data_point['id'],
                "sys_prompt": sys_prompt,
                "user_prompt": user_prompt,
                "response": response,
                'explanation': explanation_response,
                "predicted_answer": predicted_answer,
                "ground_truth": ground_truth,
                "is_correct": is_correct
            }

            results.append(obj)

        return results


    def emulsify_run(self):

        results = []
        for idx, (data_point, eng_cot_data_point, extract_data_point) in tqdm.tqdm(
                enumerate(zip(self.data, self.eng_cot_data, self.extract_data)), total=len(self.data)):
            
            assert data_point['id'] == eng_cot_data_point['id'] == extract_data_point['id']            # generate response w/ emulsify
            sys_prompt, user_prompt = EmCeiPrompting.emulsifying(data_point, eng_cot_data_point, extract_data_point, self.data_symbol, self.dataset_name)
            response = self.model.generate_response(sys_prompt, user_prompt)

            predicted_answer = self.evaluator.extract_answers(response, 'en')
            if (self.dataset_name == 'MKQA') and (data_point['answer'][0]['type'] == 'binary'): 
                predicted_answer = self.evaluator.check_binary_answer(self.data_symbol, predicted_answer)
                is_correct = None
                ground_truth = data_point['answer']
            elif self.dataset_name == 'MKQA':
                is_correct = None
                ground_truth = data_point['answer']
            else: 
                ground_truth, is_correct = self.evaluator.check_answer(
                                                data_point, 
                                                predicted_answer,
                                                self.data_symbol
                                            )

            results.append({
                "id": data_point['id'],
                "sys_prompt": sys_prompt,
                "user_prompt": user_prompt,
                "response": response,
                "predicted_answer": predicted_answer,
                "ground_truth": ground_truth,
                "is_correct": is_correct
            })

        return results

