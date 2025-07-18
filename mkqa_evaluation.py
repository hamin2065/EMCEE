import argparse
import collections
import json
import logging
import os
import sys
from gzip import GzipFile
from typing import Dict, Optional, Any

import numpy as np

import mkqa_eval_util as eval_util

MKQA_LANGUAGES = [
    "ar",
    "da",
    "de",
    "en",
    "es",
    "fi",
    "fr",
    "he",
    "hu",
    "it",
    "ja",
    "km",
    "ko",
    "ms",
    "nl",
    "no",
    "pl",
    "pt",
    "ru",
    "sv",
    "th",
    "tr",
    "vi",
    "zh_cn",
    "zh_hk",
    "zh_tw",
]

# A data structure for storing annotations
MKQAAnnotation = collections.namedtuple(
    "MKQAAnnotation",
    [
        "example_id",  # The unique ID for each example.
        "types",  # All answer types selected by inter-grader agreement
        "answers",  # All valid answer strings
    ],
)

# A data structure for storing predictions
MKQAPrediction = collections.namedtuple(
    "MKQAPrediction",
    [
        "example_id",  # The unique ID for each example.
        "prediction",  # The predicted answer text ("" serves as No Answer)
        "binary_answer",  # Is answer {"yes", "no"} (case insensitive), or `None` (indicating neither)
        "no_answer_prob",
        # (Optional) Score/probability that the answer is No Answer. Used to select the best threshold that maximizes F1.
    ],
)


def parse_args():
    parser = argparse.ArgumentParser("Official evaluation script for single language MKQA.")
    parser.add_argument(
        "-a",
        "--annotation_file",
        default='./dataset/mkaq.jsonl.gz',
        metavar="mkqa.jsonl.gz",
        # required=True,
        help="Input annotations MKQA JSON Lines gzip file.",
    )
    parser.add_argument(
        "-p",
        "--predictions_file",
        metavar="preds.json",
        # required=True,
        help="Model predictions json line file",
    )
    parser.add_argument(
        "-d",
        "--directory",
        default = './subset_data/native-basic/'
    )
    parser.add_argument(
        "-l",
        "--language",
        # required=True,
        choices=MKQA_LANGUAGES,
        help=f"Language code. Accepts any of: {MKQA_LANGUAGES}",
    )
    parser.add_argument(
        "-e",
        "--eng",
        # required=True,
        # choices=MKQA_LANGUAGES,
        help=f"Language code. Accepts any of: {MKQA_LANGUAGES}",
    )
    parser.add_argument(
        "-o",
        "--out-dir",
        metavar="results/",
        help="Write accuracy metrics to file (default is stdout).",
    )
    parser.add_argument("-v", "--verbose", action="store_true")

    parser.add_argument("--print_metrics", "-m", action="store_true", default=True)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


def read_annotations(gold_path: str) -> Dict[str, Any]:
    """Read mkqa gold annotation for all languages

    Args:
        gold_path: path to mkqa annotation file, such as mkqa.jsonl.gz

    Returns:
        A mapping from example id to MKQAAnnotation for all languages
    """
    assert os.path.exists(gold_path)

    all_gold_annotations = collections.defaultdict(dict)
    gzipped_input_file = open(gold_path, "rb")
    with GzipFile(fileobj=gzipped_input_file) as input_file:
        for line in input_file:
            example = json.loads(line)

            for language in MKQA_LANGUAGES:
                valid_answers, answer_types = [], []
                for answer in example["answers"][language]:
                    # Binary (Yes/No) answer text is always "yes" / "no"
                    # If answer['text'] is None then it `""` represents No Answer
                    valid_answers.append(answer["text"] or "")
                    valid_answers.extend(answer.get("aliases", []))
                    answer_types.append(answer["type"])

                annotation = MKQAAnnotation(
                    example_id=str(example["example_id"]),
                    types=list(set(answer_types)),
                    answers=list(set(valid_answers)),
                )

                all_gold_annotations[language][annotation.example_id] = annotation

    for lang, annotations in all_gold_annotations.items():
        if len(annotations) != 10000:
            logging.warning(
                f"The annotations file you've provided contains {len(all_gold_annotations)} for language {lang} examples, where 10000 are expected."
            )
    return all_gold_annotations


def read_predictions(predictions_path: str) -> Dict[str, MKQAPrediction]:
    """Read model prediction json file

    Args:
        predictions_path: path to prediction json line file
        {
            "example_id": <example id>,
            "prediction": <prediction text>,
            "binary_answer": <"yes", "no", "">,
            "no_answer_prob": <prob>
        }

    Returns:
        A mapping from example id to MKQAPrediction
    """
    assert os.path.exists(predictions_path)
    logging.info(f"Reading predictions from file: {predictions_path}")
    with open(predictions_path, "r") as f:
        predictions = [json.loads(l) for l in f.readlines()]

    predict_labels = {}
    for prediction in predictions:
        binary_answer = prediction["binary_answer"].lower() if prediction["binary_answer"] else None
        assert binary_answer in {
            "yes",
            "no",
            None,
        }, f"Binary prediction can only be yes, no, or None. Provided answer was {binary_answer}"

        predict_label = MKQAPrediction(
            example_id=str(prediction["example_id"]),
            prediction=prediction["prediction"] or "",
            binary_answer=binary_answer,
            no_answer_prob=prediction.get("no_answer_prob", 0),
        )

        predict_labels[predict_label.example_id] = predict_label

    return predict_labels


def compute_mkqa_scores_for_language(
    predictions: Dict[str, MKQAPrediction],
    gold_annotations: Dict[str, MKQAAnnotation],
    language: str,
) -> (Dict[str, float], Dict[str, float]):
    predict_texts, answer_texts, filtered_ids = [], [], []
    for example_id, gold_annotation in gold_annotations.items():
        if example_id in predictions:  # Only evaluate if prediction exists
            predict_texts.append(
                predictions[example_id].binary_answer or predictions[example_id].prediction
            )
            answer_texts.append(gold_annotation.answers)
            filtered_ids.append(example_id)
        else:
            logging.warning(f"Prediction for example_id {example_id} is missing. Skipping.")
    
    text_metrics = eval_util.get_text_metrics(predict_texts, answer_texts, language)
    f1_scores = {example_id: text_metrics["f1"][i] for i, example_id in enumerate(filtered_ids)}
    em_scores = {example_id: text_metrics["exact_match"][i] for i, example_id in enumerate(filtered_ids)}
    return em_scores, f1_scores

def compute_best_threshold(
    predictions: Dict[str, MKQAPrediction],
    raw_em: Dict[str, float],
    raw_f1: Dict[str, float],
    no_answer_probs: Dict[str, float],
    qid_is_answerable: Dict[str, bool],
) -> Dict[str, float]:
    """Compute the averaged text metrics at the best threshold chosen to maximize F1.
    The threshold is varied over No Answer probabilities as provided in the predictions file.

    Args:
        predictions: mapping from example id to MKQAPrediction
        raw_em: mapping from example id to em
        raw_f1: mapping from example id to f1
        no_answer_probs: mapping from example id to no_answer_probs
        qid_is_answerable: mapping from example id to boolean indicator for whether the example is answerable

    Returns:
        text metrics at the best threshold of f1
    """
    id_to_predtext = {exid: p.binary_answer or p.prediction for exid, p in predictions.items()}
    ans_em_scores = {qid: raw_em[qid] for qid in raw_em if qid_is_answerable[qid]}
    ans_f1_scores = {qid: raw_f1[qid] for qid in raw_f1 if qid_is_answerable[qid]}
    unans_em_scores = {qid: raw_em[qid] for qid in raw_em if not qid_is_answerable[qid]}

    best_scores = eval_util.compute_best_score_and_threshold(
        id_to_predtext, raw_f1, no_answer_probs, qid_is_answerable
    )
    best_f1, f1_threshold = best_scores["best_score"], best_scores["best_threshold"]

    best_em_by_id = eval_util.apply_no_answer_threshold(
        raw_em, no_answer_probs, qid_is_answerable, f1_threshold
    )

    best_answerable_em_by_id = eval_util.apply_no_answer_threshold(
        ans_em_scores, no_answer_probs, qid_is_answerable, f1_threshold
    )

    best_answerable_f1_by_id = eval_util.apply_no_answer_threshold(
        ans_f1_scores, no_answer_probs, qid_is_answerable, f1_threshold
    )

    best_unanswerable_em_by_id = eval_util.apply_no_answer_threshold(
        unans_em_scores, no_answer_probs, qid_is_answerable, f1_threshold
    )

    return {
        "best_em": round(100.0 * np.mean(list(best_em_by_id.values())), 2),
        "best_f1": round(best_f1, 2),
        "best_answerable_em": round(100.0 * np.mean(list(best_answerable_em_by_id.values())), 2),
        "best_answerable_f1": round(100.0 * np.mean(list(best_answerable_f1_by_id.values())), 2),
        "best_unanswerable_em": round(
            100.0 * np.mean(list(best_unanswerable_em_by_id.values())), 2
        ),
        "best_f1_threshold": round(f1_threshold, 2),
    }


def evaluate(
    annotations: Dict[str, MKQAAnnotation],
    predictions: Dict[str, MKQAPrediction],
    language: str,
    out_dir: Optional[str] = None,
    verbose: bool = False,
    print_metrics: bool = True,
) -> Dict[str, Any]:
    assert language in MKQA_LANGUAGES

    # Filter annotations to only those present in predictions
    filtered_annotations = {ex_id: ann for ex_id, ann in annotations.items() if ex_id in predictions}
    
    if not filtered_annotations:
        logging.error("No matching examples between annotations and predictions.")
        sys.exit(1)
    
    raw_em_scores, raw_f1_scores = compute_mkqa_scores_for_language(
        predictions, filtered_annotations, language=language
    )

    qid_is_answerable = {
        ex_id: bool(annotation.answers != [""]) for ex_id, annotation in filtered_annotations.items()
    }

    no_answer_probs = {ex_id: p.no_answer_prob for ex_id, p in predictions.items() if ex_id in filtered_annotations}

    metrics = compute_best_threshold(
        predictions, raw_em_scores, raw_f1_scores, no_answer_probs, qid_is_answerable
    )

    if print_metrics:
        # print(json.dumps(metrics, indent=4))
        print(metrics['best_f1'])
        # print(metrics['best_em'])

    if out_dir:
        with open(os.path.join(out_dir, "metrics.json"), "w") as f:
            f.write(json.dumps(metrics, indent=4))

    return metrics

# if __name__ == "__main__":

# args = parse_args()
# total = 0
# symbols = ['de', 'en', 'es', 'fr', 'ja', 'ru', 'th', 'tr', 'vi', 'zh_cn']
# for symbol in symbols:
#     print(symbol, ": ", end='')
#     directory = args.directory
#     # print(directory)
#     file_path = os.path.join(directory, f'{symbol}-predictions.jsonl')
#     symbol = file_path.split('/')[-1].split('-')[0]
#     if args.eng == True:
#         symbol = 'en'

#     annotation_file = './dataset/mkqa.jsonl.gz'
#     annotations = read_annotations(annotation_file)[symbol]
#     predictions = read_predictions(file_path)
#     metrics = evaluate(
#         annotations, predictions, symbol, args.out_dir, args.verbose,
#     )
#     total += metrics['best_f1']
# print("TOTAL: ", total)
# print("AVG: ", total/len(symbols))
