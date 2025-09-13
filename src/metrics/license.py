"""
License Score Metric
====================
Input:
- card: dict | None  (this is `info.cardData` from huggingface_hub HfApi.model_info)

Output:
- integer score in [0..5]

Rules (aligned to your spec):
- 0 = no license listed
- 5 = fully open (Apache-2.0, MIT, BSD)
- 4 = open but with some restrictions (e.g., LGPL, CC-BY)
- 3 = research/evaluation-only or non-commercial
- 1 = proprietary/closed
- 2 = fallback when license string exists but is unknown
"""

def license_score(card: dict | None) -> int:
    if not card or not card.get("license"):
        return 0
    lic = str(card["license"]).lower()
    if any(x in lic for x in ("apache-2", "apache 2", "mit", "bsd")):
        return 5
    if "lgpl" in lic or "cc-by" in lic:
        return 4
    if "research" in lic or "non-commercial" in lic or "evaluation" in lic:
        return 3
    if "proprietary" in lic or "closed" in lic:
        return 1
    return 2

