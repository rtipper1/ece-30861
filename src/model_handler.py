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
        
        # Get general model information
        info = api.model_info(self.full_name) # Contains all model information
        model_card = info.cardData  # Contains model metadata found at the beginning of the README.md for each model Note: IS A DICTIONARY
        
        self.license = self.GetModelLicense(self.full_name, api)
        self.sha = info.sha
        self.downloads = info.downloads
        self.likes = info.likes
        self.library = info.library_name
        self.base_model = model_card['base_model']
        self.inference = info.inference
        self.siblings = info.siblings
        
        
        
        # self.printSiblings()
        
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
    
    def printSiblings(self):
        print('Repo files for: '+self.full_name)
        for n in self.siblings:
            print(n)

    # Model Downloading
    # This function downloads the README from the selected model repo and stores it to the cache
    def SingleFileDownload(self, full_name, filename):
        model_path = hf_hub_download(repo_id = full_name, filename = filename, local_dir = "C:/Users/noahb/OneDrive/Documents/SCHOOL/ECE 30861/DownloadedREADMEs")
        print(f"File downloaded to: {model_path}")
        
        return model_path
    

    # downloads the entire model repository and stores it in the cache
    def fullDownload(self, full_name):
        model_path = snapshot_download(full_name)

        # print(f"Model downloaded to: {model_path}")
        
        return model_path

if __name__ == "__main__":
    owner = "google"
    model_name = "gemma-3-27b-it"
    # file = "README.md"
    model(owner, model_name)
    # GetModelInfo(model_owner=owner, model_name=model)
    # partialDownload(model_owner=owner, model_name=model, filename=file)
    
    # NO SPACE TO DOWNLOAD FULL MODEL ON ECEPROG
    # fullDownload(model_owner=owner, model_name=model)
    