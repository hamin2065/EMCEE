# import random
from dataset import Dataset
from models import GPTModel, ClaudeModel, LlamaModel
from prompt import PromptingStrategy
from evaluation import M3ExamEvaluator, MKQAEvaluator, XNLIEvaluator, XCOPAEvaluator
from typing import List, Dict
import tqdm

# random.seed(42)

class Baseline:
    """Runs baseline evaluation on datasets with different prompting strategies."""

    def __init__(self, dataset_path: str, dataset_name: str, model_type: str, strategy: str, lang_symbol: str, data_symbol: str = "en"):
        """
        :param dataset_path: Path to the dataset file.
        :param model_type: Which model to use ('gpt', 'claude', 'llama').
        :param strategy: Prompting strategy ('native-basic', 'en-basic', 'native-cot', 'en-cot', 'XLT').
        :param data_symbol: Target language for XLT (default: English).
        """
        self.dataset = Dataset(dataset_path)
        self.dataset_name = dataset_name
        self.strategy = strategy
        self.lang_symbol = lang_symbol # symbol to eval ==> "en" for en-basic, en-cot, XLT
        self.data_symbol = data_symbol
        self.data = self.dataset.load_data()
        self.model = self.load_model(model_type)
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
        return PromptingStrategy.get_prompt(self.strategy, data, self.dataset_name, self.data_symbol)

    def run(self):
        """Runs the baseline on a sample of data points."""
        # random.shuffle(self.data)
        # samples = self.data[:num_samples]

        results = []
        for idx, data_point in tqdm.tqdm(enumerate(self.data), total = len(self.data)):
            user_prompt = self.get_prompt(data_point)
            response = self.model.generate_response(sys_prompt=None, user_prompt=user_prompt)

            # Extract and evaluate the answer
            # symbol_to_eval = self.data_symbol  # Language symbol
            predicted_answer = self.evaluator.extract_answers(response, self.lang_symbol)

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
                "prompt": user_prompt,
                "response": response,
                "predicted_answer": predicted_answer,
                "ground_truth": ground_truth,
                "is_correct": is_correct
            })

        return results

