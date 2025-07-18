from typing import Dict, List, Union
import re
from rouge_score import rouge_scorer

class Evaluator:
    """Base Evaluator class defining common evaluation methods."""

    def extract_answers(self, model_response: str, symbol: str) -> Union[str, List[str]]:
        """
        Extracts answers from the model's response.
        This function should be implemented by each subclass.
        """
        raise NotImplementedError("Subclasses must implement `extract_answers`.")

    def check_answer(self, data_point: Dict, predicted_answer: Union[str, List[str]], data_symbol: str) -> bool:
        """
        Compares the model's predicted answer to the ground truth.
        This function should be implemented by each subclass.
        """
        raise NotImplementedError("Subclasses must implement `check_answer`.")
    
    @staticmethod
    def preprocess_model_answer(model_answer: str) -> str:
        """Removes special characters like '*' from the model's answer."""
        return model_answer.replace('*', '').strip()


# ================================
# Evaluator for M3Exam (Multiple Choice)
# ================================
class M3ExamEvaluator(Evaluator):
    """Evaluator for M3Exam dataset (Multiple Choice Questions)."""

    # Localized answer extraction patterns
    LOCALIZED_ANSWER_PATTERNS = {
        'en': r'Answer: (.*)',
        'zh': r'答案: (.*)',
        'it': r'Risposta: (.*)',
        'pt': r'Resposta: (.*)',
        'vi': r'Đáp án: (.*)',
        'th': r'คำตอบ: (.*)',
        'sw': r'Jibu: (.*)',
        'af': r'Antwoord: (.*)',
        'jv': r'Jawaban: (.*)',
        'en_conclusion': r'Conclusion: (.*)',
    }

    def extract_answers(self, model_response: str, symbol: str) -> str:
        """
        Extracts the predicted choice (A, B, C, D) from the response.
        """
        localized_answer_keywords = {
            'en': r'Answer: (.*)',
            'zh': r'答案: (.*)',
            'it': r'Risposta: (.*)',
            'pt': r'Resposta: (.*)',
            'vi': r'Đáp án: (.*)',
            'th': r'คำตอบ: (.*)',
            'sw': r'Jibu: (.*)',
            'af': r'Antwoord: (.*)',
            'jv': r'Jawaban: (.*)',
            'en_conclusion': r'Conclusion: (.*)',
        }
        
        # Retrieve the correct regex pattern based on the symbol
        response = Evaluator.preprocess_model_answer(model_response)
        
        pattern = localized_answer_keywords.get(symbol, 'en')
        if not pattern:
            return model_response  # Return None if the symbol is not recognized
        
        # Search for the answer in the text
        match = re.search(pattern, response)
        if match:
            return match.group(1).strip()  # Return the matched answer, stripped of extra spaces
        else:
            return model_response  # Return None if no match is found
        
    def match_symbol(self, gt, ans):
        """
        Check if the answer matches the ground truth (gt).

        Args:
        gt (str): Ground truth, expected to be a single alphabet (e.g., 'A').
        ans (str): User-provided answer string to validate.

        Returns:
        bool: True if the answer matches the ground truth, False otherwise.
        """
        if len(gt) == 1:  # gt is a single alphabet
            gt = gt.upper()  # Normalize gt to uppercase

            # Check if ans is exactly the same single alphabet
            if (len(ans) == 1) and (gt == ans.upper()):
                return True

            # Extract the content within parentheses
            match = re.search(r'\((.)\)', ans)
            if match and (match.group(1).upper() == gt):
                return True

            # Check formats like "B." or "B．"
            if ans[:2].upper() == gt + '.' or ans[:2] == gt + '．':
                return True
            if ans[:3].upper() == gt + ' .' or ans[:2] == gt + ' ．':
                return True
            # Check formats like "B)" without an opening parenthesis
            if ')' in ans and '(' not in ans:
                if len(ans) > 1 and ans[1] == ')' and ans[0].upper() == gt:
                    return True

            # Check for answers enclosed in brackets (e.g., "[B]", "{B}", etc.)
            bracket_match = re.search(r'[\[\<](.)[\]\>]', ans)
            if bracket_match and (bracket_match.group(1).upper() == gt):
                return True
            # Map ground truth letters to numbers (A=1, B=2, ..., Z=26)
            letter_to_number = {chr(i): str(i - 64) for i in range(65, 91)}  # A=1, B=2, ..., Z=26
            if gt in letter_to_number and ans == letter_to_number[gt]:
                return True

            return False
        else:
            return False
        
    def check_answer_thai(self, data_point, predicted_answer, eval_symbol):
        """
        Check if the answer matches the ground truth (gt) for Thai numerals.

        Args:
        gt (str): Ground truth, expected to be a single character (Thai or Arabic numeral).
        ans (str): User-provided answer string to validate.

        Returns:
        bool: True if the answer matches the ground truth, False otherwise.
        """
        ground_truth = data_point['ground_truth']
        if self.check_answer(data_point, predicted_answer, eval_symbol):
            return True

        # Handle cases where "x. " format exists
        if len(ans) > 1 and '. ' in ans:
            ans = ans.split('. ')[0]

        thai_to_arabic = {
            '\u0e51': '1',  # Thai 1
            '\u0e52': '2',  # Thai 2
            '\u0e53': '3',  # Thai 3
            '\u0e54': '4',  # Thai 4
            '\u0e55': '5',  # Thai 5
        }

        # Normalize gt and ans to compare both Thai and Arabic numerals
        normalized_gt = thai_to_arabic.get(predicted_answer, predicted_answer)
        normalized_ans = thai_to_arabic.get(ans, ans)

        return normalized_gt == normalized_ans


    def evaluate_text(self, model_answer, options, ground_truth):
        """
        Evaluate the model's answer using patterns and Rouge score.

        Args:
        model_answer (str): The model's predicted answer.
        options (list or str): List of possible options for the answer.
        ground_truth (str): The correct answer.

        Returns:
        str or bool: "Pattern" if a specific pattern is found, True if the best option matches the ground truth, otherwise False.
        """
        # Check for specific patterns in the model_answer
        patterns = ["(A)", "(B)", "(C)", "(D)", "A)", "B)", "C)", "D)", "A. ", "B. ", "C. ", "D. ", "A．", "B．", "C．", "D．"]
        if any(pattern in model_answer for pattern in patterns):
            return "Pattern"

        # If no pattern found, calculate Rouge score between model_answer and each option
        scorer = rouge_scorer.RougeScorer(['rouge1'], use_stemmer=True)
        highest_score = 0
        best_option = None

        for option in options:
            score = scorer.score(model_answer, option)["rouge1"].fmeasure
            if score > highest_score:
                highest_score = score
                best_option = option

        # Check if the best option matches the ground truth
        if best_option and best_option.startswith(ground_truth):
            return True
        else:
            return False
    
    def check_answer(self, data_point: Dict, predicted_answer: str, eval_symbol: str) -> bool:
        """
        Evaluate the model's answer against the ground truth.

        Args:
        ground_truth (str): The correct answer.
        model_answer (str): The model's predicted answer.
        options (list or str): Possible options for the answer.
        lang (str): Language of the evaluation (e.g., 'thai').
        is_trans (bool): Whether the options are in translated string format.

        Returns:
        bool: True if the model's answer is correct, False otherwise.
        """
        ground_truth = data_point['ground_truth']
        options = data_point['options']
        is_correct = True

        # Check answer based on language
        if eval_symbol != 'thai':
            checked = self.match_symbol(ground_truth, predicted_answer)
        else:
            checked = self.check_answer_thai(data_point, predicted_answer, eval_symbol)

        if checked:
            return ground_truth, True

        response = self.evaluate_text(predicted_answer, options, ground_truth)

        if response == "Pattern":
            # Handle pattern-based evaluation
            first_char = predicted_answer[0] if predicted_answer else ''
            if eval_symbol != 'th':
                is_correct = self.match_symbol(ground_truth, first_char)
            else:
                is_correct = self.check_answer_thai(data_point, first_char, eval_symbol)
        elif response is True:
            is_correct = True
        else:
            is_correct = False

        return ground_truth, is_correct

# ================================
# Evaluator for MKQA (Question Answering)
# ================================
class MKQAEvaluator(Evaluator):
    """Evaluator for MKQA dataset (Open-ended Question Answering)."""

    binary_translations = {
        'de': {'yes': 'Ja', 'no': 'Nein'},
        'en': {'yes': 'Yes', 'no': 'No'},
        'es': {'yes': 'Sí', 'no': 'No'},
        'fr': {'yes': 'Oui', 'no': 'Non'},
        'ja': {'yes': 'はい', 'no': 'いいえ'},
        'ru': {'yes': 'Да', 'no': 'Нет'},
        'th': {'yes': 'ใช่', 'no': 'ไม่ใช่'},
        'tr': {'yes': 'Evet', 'no': 'Hayır'},
        'vi': {'yes': 'Có', 'no': 'Không'},
        'zh_cn': {'yes': '是', 'no': '否'}
    }

    def extract_answers(self, model_response: str, symbol: str) -> str:
        """
        Extracts the main answer from the model's response.
        """
        answer_by_symbol = {
            'en': 'Answer: ',
            'de': 'Antwort: ',
            'es': 'Respuesta: ',
            'fr': 'Réponse : ',
            'ja': '回答: ',
            'ru': 'Ответ: ',
            'th': 'คำตอบ: ',
            'tr': 'Cevap: ',
            'vi': 'Trả lời: ',
            'zh_cn': '回答: '  # Fixed from 'zh_ch' to 'zh'
        }

        # Preprocess response
        response = Evaluator.preprocess_model_answer(model_response)

        # Get the localized keyword
        keyword = answer_by_symbol.get(symbol)
        if not keyword:
            return model_response  # Return original response if the symbol is not recognized

        # Regex to capture content inside brackets or plain text after the keyword
        pattern = rf"{re.escape(keyword)}\s*(?:\[)?(.*?)(?:\])?$"

        # Search for the content after the keyword
        match = re.search(pattern, response, re.IGNORECASE)
        if match:
            return match.group(1).strip()  # Return the matched content
        else:
            return model_response  # Return original response if no match is found

    def check_binary_answer(self, target_symbol, binary_answer): 
        # if (binary_answer.lower() in ("yes", "no")) or (binary_answer.lower() in self.binary_translations[target_symbol])

        if binary_answer.lower() == self.binary_translations[target_symbol]['yes'].lower():
            return "yes"
        elif binary_answer.lower() == self.binary_translations[target_symbol]['no'].lower():
            return "no"
        else: 

            # return "yes" if yes_score >= no_score else "no"
            scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)

            # Compute similarity scores
            yes_score = scorer.score(binary_answer, "yes")["rougeL"].fmeasure
            no_score = scorer.score(binary_answer, "no")["rougeL"].fmeasure

            return "yes" if yes_score >= no_score else "no"

    def check_answer(self, data_point: Dict, predicted_answer: Union[str, List[str]], symbol: str) -> bool:
        """
        Checks if the predicted answer matches any of the possible ground truths.
        MKQA may have multiple correct answers.
        """
        ground_truth = data_point['label']
        if isinstance(ground_truth, list):
            return predicted_answer.lower() in [ans.lower() for ans in ground_truth]
        return ground_truth, predicted_answer.lower() == ground_truth.lower()

# ================================
# Evaluator for XNLI (Natural Language Inference)
# ================================
import re
from typing import Optional

class XNLIEvaluator(Evaluator):
    """
    Evaluator for the XNLI dataset (Textual Entailment).
    """
    
    ANSWER_PREFIXES = {
        'en': 'Relationship: ',
        'fr': 'Relation: ',
        'es': 'Relación: ',
        'de': 'Beziehung: ',
        'el': 'Σχέση: ',
        'bg': 'Връзка: ',
        'ru': 'Связь: ',
        'tr': 'İlişki: ',
        'ar': 'العلاقة: ',
        'vi': 'Mối quan hệ: ',
        'th': 'ความสัมพันธ์: ',
        'zh': '关系：',
        'hi': 'संबंध: ',
        'sw': 'Uhusiano: ',
        'ur': 'تعلق: '
    }



    LABEL_MAPPING = {
        'en': {'entailment': 0, 'neutral': 1, 'contradiction': 2},
        'fr': {'implication': 0, 'neutre': 1, 'contradiction': 2},
        'es': {'implicación': 0, 'neutral': 1, 'contradicción': 2},
        'de': {'implikation': 0, 'neutral': 1, 'widerspruch': 2},
        'el': {'συμπερασματική': 0, 'ουδέτερη': 1, 'αντίφαση': 2},
        'bg': {'следствие': 0, 'неутрално': 1, 'противоречие': 2},
        'ru': {'следствие': 0, 'нейтрально': 1, 'противоречие': 2},
        'tr': {'çıkarım': 0, 'nötr': 1, 'çelişki': 2},
        'ar': {'استلزام': 0, 'حيادي': 1, 'تناقض': 2},
        'vi': {'kéo theo': 0, 'trung lập': 1, 'mâu thuẫn': 2},
        'th': {'ตามมา': 0, 'เป็นกลาง': 1, 'ขัดแย้ง': 2},
        'zh': {'蕴含': 0, '中立': 1, '矛盾': 2},
        'hi': {'निष्कर्ष': 0, 'तटस्थ': 1, 'विरोधाभास': 2},
        'sw': {'ulinganifu': 0, 'wastani': 1, 'mpingano': 2},
        'ur': {'نتیجہ اخذ': 0, 'غیر جانبدار': 1, 'تضاد': 2}
    }
    
    @staticmethod
    def clean_answer(answer: str) -> str:
        """
        Cleans the extracted answer by removing punctuation and extra spaces.
        """
        answer = re.sub(r"[.,!?;:\"'“”‘’\[\](){}<>，。！？；：「」【】]", '', answer)
        return re.sub(r'\s+', ' ', answer).strip().lower()
    
    def extract_answers(self, model_response: str, symbol: str):
        """
        Extracts the model's predicted answer and maps it to a label based on the given language symbol.
        """

        if (symbol == 'en') and (model_response.lower() in ('contradiction', 'entailment', 'neutral')):
            return self.LABEL_MAPPING['en'][model_response.lower()]
        keyword = self.ANSWER_PREFIXES.get(symbol)
        if not keyword:
            return model_response  # Return original response if prefix not found

        # Regex pattern to extract the response after the prefix
        pattern = rf"{re.escape(keyword)}\s*(?:\[|【)?(.*?)(?:\]|】)?$"
        match = re.search(pattern, model_response, re.IGNORECASE)

        if match:
            extracted_answer = self.clean_answer(match.group(1))  # Extract and clean the answer
            return self.LABEL_MAPPING.get(symbol, {}).get(extracted_answer, extracted_answer)  # Map answer or return original

        return model_response  # Return original if no match

    @staticmethod
    def check_answer(data_point: Dict, predicted_answer: str, symbol: str) -> bool:
        """
        Checks if the predicted entailment label matches the ground truth.
        """
        ground_truth = data_point['label']
        return ground_truth, predicted_answer == ground_truth

# ================================
# Evaluator for XCOPA (Causal Commonsense Reasoning)
# ================================
class XCOPAEvaluator(Evaluator):
    """
    Evaluator for the XCOPA dataset (Causal Reasoning).
    """
    
    # Patterns for extracting answers in various languages
    ANSWER_PATTERNS = {
        'xlt': r'Choice number[:：\uff1a]\s*\[?([1-2])\]?',
        'et': r'Vastus[:：\uff1a]\s*\[?([1-2])\]?',
        'ht': r'Repons[:：\uff1a]\s*\[?([1-2])\]?',
        'id': r'Jawaban[:：\uff1a]\s*\[?([1-2])\]?',
        'it': r'Risposta[:：\uff1a]\s*\[?([1-2])\]?',
        'qu': r'Kutichiy[:：\uff1a]\s*\[?([1-2])\]?',
        'sw': r'Jibu[:：\uff1a]\s*\[?([1-2])\]?',
        'ta': r'\u0baa\u0ba4\u0bbf\u0bb2[:：\uff1a]\s*\[?([1-2])\]?',
        'th': r'\u0e04\u0e33\u0e15\u0e2d\u0e1a[:：\uff1a]\s*\[?([1-2])\]?',
        'tr': r'Cevap[:：\uff1a]\s*\[?([1-2])\]?',
        'vi': r'Câu trả lời[:：\uff1a]\s*\[?([1-2])\]?',
        'zh': r'答案[:：\uff1a]\s*\[?([1-2])\]?',
        'en': r'Answer[:：\uff1a]\s*\[?([1-2])\]?',
    }

    def extract_answers(self, model_response: str, symbol: str) -> Optional[int]:
        """
        Extracts the answer (1 or 2) from a response in different languages.
        
        Parameters:
            model_response (str): The response string.
            symbol (str): The language symbol (e.g., 'et', 'id').
            
        Returns:
            int: 1 or 2 if found, else None.
        """
        pattern = self.ANSWER_PATTERNS.get(symbol, self.ANSWER_PATTERNS['en'])
        match = re.search(pattern, model_response, re.IGNORECASE)
        return int(match.group(1)) if match else model_response

    @staticmethod
    def check_answer(data_point: Dict, predicted_answer: Optional[int], symbol) -> bool:
        """
        Checks if the predicted choice matches the correct one.
        
        Parameters:
            predicted_answer (Optional[int]): The extracted choice (1 or 2).
            ground_truth (int): The correct answer (0 or 1).
            
        Returns:
            bool: True if the predicted answer is correct, False otherwise.
        """
        ground_truth = int(data_point['label'])
        try: 
            predicted_answer = int(predicted_answer)
            return ground_truth, predicted_answer is not None and (predicted_answer - 1) == ground_truth
        except:
            return ground_truth, False