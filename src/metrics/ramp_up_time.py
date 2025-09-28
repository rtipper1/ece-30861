"""
ramp_up_time.py
---------------
Ramp Up Time Metric.

Summary
- Estimates ease of adoption for developers using the model.
- Considers availability of documentation, tutorials, and example code.
- Maps estimated learning curve (minutes to days) into a [0,1] score.
- Calculates latency of the scoring process to support performance reporting.
"""

import os
from typing import Dict

import requests

from src.cli.url import ModelURL
from src.metrics.metric import Metric


class RampUpTimeMetric(Metric):
    def __init__(self, model_url: ModelURL):
        super().__init__("ramp_up_time")
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
                    "content": f"""You are tasked with evaluating a Hugging Face model’s README file for ramp-up time. 
                                    Model URL: {self.model_url.raw}
                                    Ramp-up time is defined as the amount of effort and time it would take a new user, 
                                    with basic machine learning knowledge but no prior familiarity with this specific model, 
                                    to successfully install, load, and begin using the model in a real workflow.  

                                    When scoring, consider the following factors:  

                                    1. Installation & Setup Clarity  
                                    - Are installation instructions provided (e.g., pip install or environment setup)?  
                                    - Are dependencies clearly listed and easy to install?  
                                    - Is there a requirements file or environment specification?  

                                    2. Quickstart Examples  
                                    - Is there a clear code snippet showing how to load the model and run inference?  
                                    - Does the example work out of the box, or does it require significant modification?  
                                    - Are both minimal and more advanced usage examples included?  

                                    3. Documentation Quality  
                                    - Are input formats and output formats described (e.g., tensor shapes, text formats, preprocessing steps)?  
                                    - Are common pitfalls or errors addressed?  
                                    - Is there guidance on fine-tuning, customization, or integration?  

                                    4. Resource Requirements  
                                    - Does the README mention hardware or software requirements (e.g., GPU, memory)?  
                                    - Are there lightweight alternatives or guidance for limited environments?  

                                    5. Supporting Materials  
                                    - Are links to tutorials, demos, or notebooks provided?  
                                    - Are external references (e.g., related papers or blog posts) linked to help users understand context?  

                                    6. Completeness & Accessibility  
                                    - Is the README self-contained enough for a motivated user to get started quickly?  
                                    - Is the language clear, free of heavy jargon, and beginner-friendly?  
                                    - Are key steps or commands missing that would slow a user down?  

                                    Your task: Provide a rating (float([0-1]), where 0 = very high ramp-up difficulty and 1 = very easy ramp-up).
                                    IMPORTANT: output only this float rating. Do not provide any context or thought process.
                                """
                }
            ],
        }

        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            response_data = response.json()

            output = response_data["choices"][0]["message"]["content"]
            score = float(output)
            return {
                "score": score,
            }

        except (ValueError, KeyError) as e:
            print(f"Error extracting outputL {e}")
