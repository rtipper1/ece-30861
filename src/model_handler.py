from huggingface_hub import HfApi, ModelCard, snapshot_download

api = HfApi()
# or:
info = api.model_info("LLM360/K2-Think")
print(info.id, info.sha, info.cardData)

# Model Downloading

