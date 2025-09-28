"""
dataset_and_code.py
-------------------
Dataset and Code Availability Metric.

Summary
- Estimates quality and availability of dataset and code for a model.
- Considers dataset documentation, benchmarks, and example usage.
- Evaluates clarity and completeness of provided training/evaluation resources.
- Maps overall availability/quality into a [0,1] score.
"""

from src.metrics.metric import Metric
from typing import Dict
from src.cli.url import ModelURL
import requests
import os


class DatasetAndCodeMetric(Metric):
    def __init__(self, model_url: ModelURL):
        super().__init__("dataset_and_code_score")
        self.model_url = model_url

    def calculate_score(self) -> float:
        return self.data["score"]

    def get_data(self) -> Dict[str, float]:
        api_key = os.environ.get("GEN_AI_STUDIO_API_KEY")
        if not api_key:
            raise Exception("API key not set")

        if not self.model_url:
            return {"score": 0.0}

        url = "https://genai.rcac.purdue.edu/api/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "model": "llama3.1:latest",
            "messages": [
                {
                    "role": "user",
                    "content": f"""You are tasked with evaluating a Hugging Face model’s README file 
                                    for dataset and code quality. 
                                    Model URL: {self.model_url.raw}

                                    When scoring, consider the following factors:

                                    1. Dataset Documentation
                                    - Is the dataset used for training or benchmarking clearly described?
                                    - Are details about data collection, preprocessing, and licensing provided?
                                    - Are benchmarks reproducible?

                                    2. Dataset Availability
                                    - Is the dataset publicly accessible?
                                    - Are download instructions or links available and reliable?
                                    - Are subsets or samples provided for quick testing?

                                    3. Code Quality
                                    - Is example code provided for training, evaluation, or inference?
                                    - Is the code clean, documented, and easy to reuse?
                                    - Are scripts or notebooks provided for common workflows?

                                    4. Completeness & Transparency
                                    - Are limitations, biases, or ethical considerations documented?
                                    - Is the dataset size and diversity explained?
                                    - Are citations or references included?

                                    Your task: Provide a rating (float in [0-1], 
                                    where 0 = very poor dataset/code quality and 1 = excellent dataset/code quality).
                                    IMPORTANT: output only this float rating. Do not provide any context or explanation.
                                """
                }
            ],
        }

        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            response_data = response.json()

            output = response_data["choices"][0]["message"]["content"]
            score = float(output.strip())

            return {
                "score": score,
            }

        except (ValueError, KeyError) as e:
            print(f"Error extracting output: {e}")
            return {"score": 0.0}
