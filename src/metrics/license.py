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

level_5_licenses = ["apache-2.0", "mit", "bsd", "bsd-2-clause", "bsd-3-clause",
    "bsd-3-clause-clear", "isc", "zlib", "unlicense", "cc0-1.0",
    "wtfpl", "postgresql", "ncsa", "afl-3.0", "artistic-2.0",
    "ecl-2.0", "mpl-2.0", "ms-pl", "etalab-2.0", "odc-by",
    "odbl", "eupl-1.1", "eupl-1.2", "epl-1.0", "epl-2.0",
    "lppl-1.3c", "ofl-1.1", "pddl", "cdla-permissive-1.0",
    "cdla-permissive-2.0", "cdla-sharing-1.0"]
level_4_licenses = ["lgpl", "lgpl-2.1", "lgpl-3.0", "cc-by-4.0", "cc-by-3.0",
    "cc-by-2.0", "cc-by-2.5", "cc-by-sa-4.0", "cc-by-sa-3.0",
    "cc", "osl-3.0", "bsl-1.0", "gpl", "gpl-2.0", "gpl-3.0",
    "agpl-3.0", "gfdl"]
level_3_licenses = ["cc-by-nc-4.0", "cc-by-nc-3.0", "cc-by-nc-2.0", "cc-by-nc-sa-4.0",
    "cc-by-nc-sa-3.0", "cc-by-nc-sa-2.0", "cc-by-nc-nd-4.0",
    "cc-by-nc-nd-3.0", "fair-noncommercial-research-license",
    "intel-research", "h-research"]
level_2_licenses = ["openrail", "openrail++", "creativeml-openrail-m", "bigscience-bloom-rail-1.0",
    "bigscience-openrail-m", "bigcode-openrail-m", "deepfloyd-if-license",
    "apple-amlr", "apple-ascl", "lgpl-lr", "open-mdw", "c-uda"]
level_1_licenses = ["llama2", "llama3", "llama3.1", "llama3.2", "llama3.3",
    "llama4", "gemma"]


def license_score(model_owner, model_name) -> int:
    
    api = HfApi() # make huggingface api connection
    full_name = model_owner + "/" + model_name # contains full model name: owner/model_name
    info = api.model_info(full_name)
    
    print(info.cardData)
    
    if info.cardData.license_name != None:
        lic = info.cardData.license_name
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
