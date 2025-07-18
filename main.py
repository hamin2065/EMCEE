import argparse, os, json
from baselines import Baseline
from emcei import EmCei

from mkqa_evaluation import read_annotations, read_predictions, evaluate

def show_results(dataset_name: str, save_folder_path: str, data_symbol, eval_symbol): 

    with open(os.path.join(save_folder_path, f"{data_symbol}-test.json"), "r") as f:
        results = json.load(f)

    if dataset_name != 'MKQA': 
        return sum(1 for item in results if item.get("is_correct") == True)

    elif dataset_name == 'MKQA': 
        # make list of json objects into jsonl file (for MKQA evaluation file)
        file_path = os.path.join(save_folder_path, f"{data_symbol}-test.jsonl")
        with open(file_path, "w") as f:
            for item in results:
                if item['ground_truth'][0]['type'] == 'binary': # if answer type is binary
                    jsonl_entry = {
                        'example_id': item['id'],
                        'response': item['response'],
                        'prediction': None,
                        'binary_answer': item['predicted_answer'],
                        'no_answer_prob': 0
                    }
                else: # answer type is NOT binary. 
                    jsonl_entry = {
                        'example_id': item['id'],
                        'response': item['response'],
                        'prediction': item['predicted_answer'],
                        'binary_answer': None,
                        'no_answer_prob': 0
                    }

                f.write(json.dumps(jsonl_entry) + "\n")

        annotation_file = './data/MKQA/mkqa.jsonl.gz' # check location!
        annotations = read_annotations(annotation_file)[eval_symbol]
        predictions = read_predictions(file_path)

        metrics = evaluate(
            annotations, predictions, eval_symbol
        )

        return metrics['best_f1']

def main():
    """Parses command-line arguments and runs the baseline evaluation."""
    parser = argparse.ArgumentParser(description="Run AI model evaluation on various datasets.")

    # Required arguments
    parser.add_argument("--dataset_path", type=str, required=True, 
                        help="Path to dataset file (e.g., data/m3exam.json)")
    parser.add_argument("--dataset_name", type=str, required=True, choices=["M3Exam", "MKQA", "XNLI", "XCOPA"],
                        help="Dataset name")
    parser.add_argument("--model", type=str, choices=["gpt", "claude", "llama"], required=True, 
                        help="Model to use: gpt, claude, or llama")
    parser.add_argument("--strategy", type=str, choices=["native-basic", "en-basic", "native-cot", "en-cot", "XLT", "extract", "emulsify"], required=True, 
                        help="Prompting strategy: native-basic, en-basic, native-cot, en-cot, XLT, extract, emulsify")

    # Optional arguments
    parser.add_argument("--data_symbol", type=str, default="en", 
                        help="Native language symbol to test")
    parser.add_argument("--eval_symbol", type=str, default="en", 
                        help="'en' if strategy in ('EN-BASIC', 'EN-COT', 'XLT')")
    parser.add_argument("--eng_cot_path", type=str, 
                        help="Path to English CoT results file (Required for 'emulsify' strategy)")
    parser.add_argument("--extract_path", type=str, 
                        help="Path to English CoT results file (Required for 'emulsify' strategy)")
    
    args = parser.parse_args()

    # Enforce rules for strategies
    if args.strategy == "XLT" and args.data_symbol == "en":
        print("Warning: --data_symbol is ignored unless --strategy is set to XLT.")

    if args.strategy == "emulsify" and not args.eng_cot_path:
        parser.error("Error: 'emulsify' strategy requires '--eng_cot_path'. 'en-cot' must be run first.")
    if args.strategy == "emulsify" and not args.extract_path:
        parser.error("Error: 'emulsify' strategy requires '--extract_path'. 'extract' must be run first.")


    # Run Baseline
    if args.strategy in ["native-basic", "en-basic", "native-cot", "en-cot", "XLT"]: 
        baseline = Baseline(args.dataset_path, args.dataset_name, args.model, args.strategy, args.eval_symbol, args.data_symbol)
        results = baseline.run()
    elif args.strategy in ["extract", "emulsify"]: 
        emcei = EmCei(
            args.dataset_path, 
            args.dataset_name, 
            args.eng_cot_path,
            args.extract_path,
            args.model, 
            args.strategy, 
            args.eval_symbol,
            args.data_symbol
            )

        if args.strategy == 'extract': 
            results = emcei.extract_run()
        elif args.strategy == 'emulsify':
            results = emcei.emulsify_run()
    else: 
        # error
        valid_strategies = ["native-basic", "en-basic", "native-cot", "en-cot", "XLT", "extract", "emulsify"]
        raise ValueError(f"Invalid strategy '{args.strategy}'. Supported strategies are: {valid_strategies}")

    save_folder_path = f"./results/{args.dataset_name}/{args.model}/{args.strategy}/"
    if not os.path.exists(save_folder_path):
        os.makedirs(save_folder_path)

    with open(os.path.join(save_folder_path, f"{args.data_symbol}-test.json"), "w") as f:
        json.dump(results, f, indent=4)

    ### show results ###
    score = show_results(
        dataset_name = args.dataset_name,
        save_folder_path = save_folder_path,
        data_symbol = args.data_symbol,
        eval_symbol = args.eval_symbol
    )
    print(score)

if __name__ == "__main__":
    main()
