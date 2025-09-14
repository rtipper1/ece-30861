from huggingface_hub import HfApi, ModelCard, snapshot_download

api = HfApi()
# or:
info = api.model_info("LLM360/K2-Think")
print(info.id, info.sha, info.cardData)

# Model Downloading

def modelDownload(id):
    ###  WARNING CODE FROM CHAT GPT, REQUIRES FURTHER TESTING
    model_path = snapshot_download(repo_id="distilbert-base-uncased")

    print(f"Model downloaded to: {model_path}")
    ###
    
    
if __name__ == "__main__":
    modelPath = "LLM360/K2-Think"
    modelDownload(id = modelPath)