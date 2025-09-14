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
def partialDownload(model_owner, model_name, filename):
    full_name = model_owner + "/" + model_name # contains full model name: owner/model_name
    model_path = hf_hub_download(repo_id = full_name, filename = "README.md")

    print(f"Model downloaded to: {model_path}")
   

# downloads the entire model repository and stores it in the cache
def fullDownload(model_owner, model_name):
    full_name = model_owner + "/" + model_name # contains full model name: owner/model_name
    model_path = snapshot_download(full_name)

    print(f"Model downloaded to: {model_path}")

if __name__ == "__main__":
    owner = "LLM360"
    model = "K2-Think"
    file = "README.md"
    
    testGetModelInfo(model_owner=owner, model_name=model)
    partialDownload(model_owner=owner, model_name=model, filename=file)
    
    # NO SPACE TO DOWNLOAD FULL MODEL ON ECEPROG
    # fullDownload(model_owner=owner, model_name=model)
    