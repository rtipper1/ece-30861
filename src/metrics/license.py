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
from huggingface_hub import HfApi, ModelCard

def license_score(model_owner, model_name) -> int:
    
    api = HfApi() # make huggingface api connection
    full_name = model_owner + "/" + model_name # contains full model name: owner/model_name
    info = api.model_info(full_name)
    
    print(info.cardData)
    
    if "license_name" in info.cardData:
        lic = info.cardData.license_name
        print("bong")
    else:
        lic = info.cardData.license
    
    print('license: ', lic)
    if lic == None:
        return 0
    elif any(x in lic for x in ("apache-2", "apache 2", "mit", "bsd")):
        return 5
    elif "lgpl" in lic or "cc-by" in lic:
        return 4
    elif "research" in lic or "non-commercial" in lic or "evaluation" in lic:
        return 3
    elif "proprietary" in lic or "closed" in lic:
        return 2
    else:
        return 1

# Main file for testing
if __name__ == "__main__":
    owner = "fcdalgic"
    model = "demooo"
    score = license_score(model_owner=owner, model_name=model)
    print('Score: ', score)
