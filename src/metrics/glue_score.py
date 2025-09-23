"""
glue_score.py
---------------
Dataset and Code Availability Metric.

Summary
- Implements GLUE-based scoring for dataset/documentation/code linkage.
- Applies higher weight to datasets aligned with model’s intended function.
- Computes dataset_and_code_score field.
"""

from src.metrics.metric import Metric
from huggingface_hub import HfApi

GLUE_TASKS = [
    "glue", "mnli", "qnli", "qqp", "sst2", "cola", "mrpc", "stsb", "rte", "wnli"
]

class GlueScoreMetric(Metric):
    def __init__(self, model_url=None):
        super().__init__("dataset_and_code_score")
        self.model_url = model_url

    def get_data(self):
        """Fetch metrics and README text for this model."""
        api = HfApi()
        info = api.model_info(f"{self.model_url.author}/{self.model_url.name}")
        metrics = info.cardData.get("metrics") if info.cardData else []
        readme_text = ""
        try:
            card = api.model_card(f"{self.model_url.author}/{self.model_url.name}")
            readme_text = card.text or ""
        except Exception:
            pass
        return {"metrics": metrics, "readme": readme_text}

    def calculate_score(self) -> int:
        metrics = self.data.get("metrics") or []
        readme = (self.data.get("readme") or "").lower()

        # 1) check structured GLUE value
        glue_val = None
        for m in metrics:
            name = str(m.get("name", "")).lower()
            if "glue" in name and "value" in m:
                glue_val = float(m["value"])
                break

        if glue_val is not None:
            if glue_val >= 90:
                return 5
            elif glue_val >= 80:
                return 4
            elif glue_val >= 60:
                return 3
            elif glue_val >= 40:
                return 2
            else:
                return 1

        # 2) fallback: README mentions GLUE/subtasks → partial credit
        if any(task in readme for task in GLUE_TASKS):
            return 2

        # 3) no evidence at all
        return 0

if __name__ == "__main__":
    from src.cli.cli import URL

    # pick a model that is known to have GLUE evaluation
    # you may need to experiment; some BERT/RoBERTa variants usually have GLUE
    url = URL(author="nyu-mll", name="roberta-base-1B-GLUE")

    metric = GlueScoreMetric(model_url=url)
    metric.run()   # assuming Metric base sets self.data and then calls calculate_score

    print("Fetched data:", metric.data)
    print("Calculated GLUE score:", metric.score)
