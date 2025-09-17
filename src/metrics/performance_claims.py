"""
performance_claims.py
-----------------------
Performance Claims Metric

Summary:
- Analyzes model card or README for reported benchmarks/evaluations.
- Validates whether claims are supported with evidence.
- Penalizes bold or contradictory claims without citations.

Two entrypoints:
- performance_claims_from_readme(text): score using README text.
- performance_claims_from_api(repo_id): fetch README text via HfApi().model_card and score it.

Scoring (coarse; tighten later):
- Count mentions of benchmark-y keywords. Map hits: 0→1, 1→2, 2→3, 3→4, ≥4→5.
"""

# from huggingface_hub import HfApi

# _KEYWORDS = ("benchmark", "mmlu", "leaderboard", "eval", "accuracy") # add more

# def performance_claims_from_readme(text: str | None) -> int:
#     t = (text or "").lower()
#     hits = sum(k in t for k in _KEYWORDS)
#     if hits == 0: return 1
#     if hits == 1: return 2
#     if hits == 2: return 3
#     if hits == 3: return 4
#     return 5

# def performance_claims_from_api(repo_id: str) -> int:
#     try:
#         card = HfApi().model_card(repo_id)
#         return performance_claims_from_readme(card.text)
#     except Exception:
#         return 1

from .metric import Metric

class PerformanceClaimsMetric(Metric):
    def __init__(self):
        super().__init__("performance_claims")

    def calculate_score(self) -> float:
        return 0.0