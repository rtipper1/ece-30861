from huggingface_hub import HfApi, ModelCard

api = HfApi()
# or:
info = api.model_info("LLM360/K2-Think")
print(info.id, info.sha, info.cardData)
