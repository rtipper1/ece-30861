"""
model_handler.py
----------------
Model Handler for Metadata Collection.

Summary
- Given a Hugging Face model URL, fetches metadata via the API and clones the repo locally.
- Aggregates API data (downloads, likes, last modified, file list) and repo data (README, LICENSE, weights).
- Returns a unified data structure consumable by all metric classes.
- Bridges CLI input to the metrics subsystem while keeping concerns separated.

Output data structure could look something like this in dictionary format

 metadata = {
            "url": self.url,
            "model_id": 234587234,
            "downloads": 400000,
            "likes": 250000,
            "last_modified": "9/27/25",
            "card_data": api_data["card_data"],
            "files": api_data["siblings"],  # list of files in repo
            "local_repo": local_repo,       # path to cloned repo
        }
"""

from huggingface_hub import HfApi, ModelCard, snapshot_download, hf_hub_download

class model:
    def __init__(self, model_owner, model_name):
        self.full_name = model_owner + "/" + model_name # Full model name
        api = HfApi()
        
        self.license = self.GetModelLicense(self.full_name, api)
        
    # This function gets a models info from the Model Card
    def GetModelLicense(self, full_name, api):
        info = api.model_info(full_name)
        # Gets license stores under either license or license_name
        # Changes from model to model so we need to check both
        if info.cardData.license_name != None:
            license = info.cardData.license_name
        else:
            license = info.cardData.license
        return license
        

    # Model Downloading
    # This function downloads the README from the selected model repo and stores it to the cache
    def SingleFileDownload(self, model_owner, model_name, filename):
        full_name = model_owner + "/" + model_name # contains full model name: owner/model_name
        model_path = hf_hub_download(repo_id = full_name, filename = filename)
        # print(f"File downloaded to: {model_path}")
        
        return model_path
    

    # downloads the entire model repository and stores it in the cache
    def fullDownload(self, model_owner, model_name):
        full_name = model_owner + "/" + model_name # contains full model name: owner/model_name
        model_path = snapshot_download(full_name)

        print(f"Model downloaded to: {model_path}")
        
        return model_path

if __name__ == "__main__":
    owner = "raidium"
    model_name = "curia"
    # file = "README.md"
    model(owner, model_name)
    # GetModelInfo(model_owner=owner, model_name=model)
    # partialDownload(model_owner=owner, model_name=model, filename=file)
    
    # NO SPACE TO DOWNLOAD FULL MODEL ON ECEPROG
    # fullDownload(model_owner=owner, model_name=model)
    