import json
from typing import List, Dict


class Dataset:

    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path

    def load_data(self) -> List[Dict]:
        try:
            with open(self.dataset_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)

            if isinstance(raw_data, dict):
                return [{"id": key, **value} for key, value in raw_data.items()]
            elif isinstance(raw_data, list):
                return raw_data
            else:
                raise ValueError("Unexpected dataset format. Expected list or dictionary with index keys.")

        except Exception as e:
            raise RuntimeError(f"Error loading dataset: {e}")