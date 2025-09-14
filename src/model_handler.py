from huggingface_hub import HfApi, ModelCard, snapshot_download, hf_hub_download

# This function gets a models info from the Model Card
def testGetModelInfo(model_owner, model_name):
    api = HfApi()
    # or:
    full_name = model_owner + "/" + model_name # contains full model name: owner/model_name
    info = api.model_info(full_name)
    print(info.id, info.sha, info.cardData)

# Model Downloading
# This function downloads the README from the selected model repo and stores it to the cache
def modelDownload(model_owner, model_name):
    full_name = model_owner + "/" + model_name # contains full model name: owner/model_name
    model_path = hf_hub_download(repo_id = full_name, filename = "README.md")

    print(f"Model downloaded to: {model_path}")
   
    
    
if __name__ == "__main__":
    owner = "tencent"
    model = "SRPO"
    
    testGetModelInfo(model_owner=owner, model_name=model)
    modelDownload(model_owner=owner, model_name=model)
    