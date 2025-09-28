"""
dataset_quality.py
--------------------
Dataset Quality Metric.

Summary
- Evaluates datasets linked to the model by prompting an AI.
- Considers documentation, peer review, community adoption, and transparency.
- Normalizes dataset quality into [0,1].
"""

from src.metrics.metric import Metric
from src.cli.url import DatasetURL, CodeURL
from typing import Dict
import requests
import os


class DatasetQualityMetric(Metric):
    def __init__(self, dataset_url: DatasetURL):
        super().__init__("dataset_quality")
        self.dataset_url = dataset_url

    def calculate_score(self) -> float:
        return self.data["score"]

    def get_data(self) -> Dict[str, float]:
        api_key = os.environ.get("API_KEY")
        if not api_key:
            raise Exception("API key not set")

        if not self.dataset_url:
            return {"score": 0.0}

        url = "https://genai.rcac.purdue.edu/api/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        body = {
            "model": "llama3.1:latest",
            "messages": [
                {
                    "role": "user",
                    "content": f"""You are tasked with evaluating the quality of a Hugging Face dataset.
                                    Dataset URL: {self.dataset_url.raw}

                                    Consider the following factors:

                                    1. Documentation
                                    - Is the dataset clearly described with purpose, structure, and usage?
                                    - Are preprocessing steps, licensing, and benchmarks documented?

                                    2. Availability & Transparency
                                    - Is the dataset accessible and easy to use?
                                    - Are limitations, biases, or ethical considerations discussed?

                                    3. Community & Peer Review
                                    - Has the dataset been cited, reviewed, or widely adopted?
                                    - Are references or comparisons to similar datasets provided?

                                    4. Supporting Code
                                    - Is example code for using or evaluating the dataset included?

                                    Your task: Provide a rating as a float in [0,1], 
                                    where 0 = very poor dataset quality and 1 = excellent dataset quality.
                                    IMPORTANT: Output only the float rating. Do not provide any context or explanation.
                                """,
                }
            ],
        }

        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            response_data = response.json()

            output = response_data["choices"][0]["message"]["content"]
            score = float(output.strip())
            return {"score": score}

        except (ValueError, KeyError) as e:
            print(f"Error extracting dataset quality score: {e}")
            return {"score": 0.0}

    