"""
dataset_quality.py
--------------------
Dataset Quality Metric.

Summary
- Evaluates datasets linked to the model.
- Scores based on documentation availability, peer review, and community adoption.
- Normalizes score in [0,1] according to rubric criteria.

Rubric:
- 0.2 = Only 1 significant phrase found
- 0.4 = Only 2 significant phrases found
- 0.6 = Only 3 significant phrases found
- 0.8 = Only 4 significant phrases found
- 1 = All 5 significant phrases found
"""

from src.metrics.metric import Metric
from src.cli.url import DatasetURL, CodeURL
from huggingface_hub import HfApi, hf_hub_download
from typing import Dict
import tempfile


sigPhrases = ["social impact", "bias", "limitations", "license", "comparison"]
'''
Step 1: Get dataset README.md
Step 2: Isolate lines in README
Step 3: Iterate Over Lines
Step 4: Inside that iteration, iterate over phrases in sigPhrases list
Step 5: If a significant phrase is found in the line, remove the phrase from the list and keep add on to count
'''

class DatasetQualityMetric(Metric):
    def __init__(self, code_url: CodeURL, dataset_url: DatasetURL):
        super().__init__("dataset_quality")
        self.code_url = code_url
        self.dataset_url = dataset_url

    def calculate_score(self) -> float:
        if self.data["score"] == None:
            return 0.0
            

        # Retrieve score from metric data
        score = self.data["score"]
        
        # Score metric based on categories
        if score == 5:
            return 1

        elif score == 4:
            return 0.8

        elif score == 3:
            return 0.6

        elif score == 2:
            return 0.4

        elif score == 1:
            return 0.2

        else:
            return 0.0
    
    
    def get_data(self) -> Dict[str, int]:
        temp_dir = tempfile.TemporaryDirectory()
        full_name = f"{self.dataset_url.author}/{self.dataset_url.name}" # Full model name
        file_path = self.SingleFileDownload(full_name= full_name, filename="README.md", landingPath=temp_dir.name)
        count = 0
        phrases = sigPhrases
        # Parse README.md for significant phrases
        f = open(file_path, "r")
        lines = f.readlines()
        for line in lines:
            index = 0
            line = line.lower()
            for phrase in phrases:
                index += 1
                if phrase in line:
                    count += 1
                    phrases.pop(index)
        f.close()
        temp_dir.cleanup()
        
        return {"score": count}
        
        
    def SingleFileDownload(self, full_name : str, filename : str, landingPath : str):
        # full_name = model_owner + "/" + model_name # Full model name    
        model_path = hf_hub_download(repo_id = full_name, filename = filename, local_dir = landingPath)
        # print(f"File downloaded to: {model_path}")
        
        return model_path
    