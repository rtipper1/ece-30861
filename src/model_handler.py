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

from huggingface_hub import HfApi, ModelCard, snapshot_download, hf_hub_download, RepoUrl
from dataclasses import dataclass
from flake8.api import legacy as flake8

# Turning class into @dataclass
# Model Data
@dataclass
class LicenseData:
    license : str

@dataclass
class SizeData:
    size : int
    
@dataclass
class RampUpTimeData:
    rampUpTime : int

@dataclass
class BusFactorData:
    contributors : int

@dataclass
class GlueScoreData:
    glueScore : float
    
@dataclass
class DatasetQualityData:
    numSigPhrases : int
    
@dataclass
class CodeQualityData:
    issues : int
    linesOfCode : int

@dataclass
class PerformanceClaimsData:
    likes : int
    downloads : int

# General HuggingFace API  connection
api = HfApi()

 # This function gets a models info from the Model Card
def GetModelLicense(model_owner : str, model_name : str):
    full_name = model_owner + "/" + model_name # Full model name    
    info = api.model_info(full_name)
    # Gets license stores under either license or license_name
    # Changes from model to model so we need to check both
    if info.cardData.license_name != None:
        license = info.cardData.license_name
    else:
        license = info.cardData.license
    return LicenseData(license)

# Could be changed later to get tensor type as well
def GetParameters(model_owner : str, model_name : str):
    full_name = model_owner + "/" + model_name # Full model name    
    info = api.model_info(full_name)
    st = info.safetensors
    params = st.total
    return SizeData(size = params)

def GetRampUpTime(model_owner : str, model_name : str):
    dummy = 0

def GetBusFactor(model_owner : str, model_name : str):
    dummy = 0

def GetGlueScore(model_owner : str, model_name : str):
    dummy = 0

sigPhrases = ["social impact", "bias", "limitations", "license", "comparison"]
'''
Step 1: Get dataset README.md
Step 2: Isolate lines in README
Step 3: Iterate Over Lines
Step 4: Inside that iteration, iterate over phrases in sigPhrases list
Step 5: If a significant phrase is found in the line, remove the phrase from the list and keep add on to count
'''
def GetDatasetQuality(model_owner : str, model_name : str):
    # Get readme
    full_name = model_owner + "/" + model_name # Full model name    
    file_path = SingleFileDownload(full_name= full_name, filename="README.md", landingPath="C:/Users/noahb/OneDrive/Documents/SCHOOL/ECE 30861/DownloadedREADMEs")
    print(file_path)
    count = 0
    phrases = sigPhrases
    # Parse README.md for significant phrases
    f = open(file_path, "r")
    lines = f.readlines()
    for line in lines:
        index = 0
        line = line.lower()
        for phrase in phrases:
            index += 1
            if phrase in line:
                count += 1
                phrases.pop(index)
    f.close()
    return DatasetQualityData(numSigPhrases= count)

'''
Step 1: Make list of Repo Files
Step 2: Check if each file is a .py file
Step 3: Add .py files to a list
Step 4: Add the number of lines in each .py file to the LoC variable
Step 5: If no .py file in the model then go to the listed base model and redo steps 2 - 4
Step 6: If there are no .py files found then return issues and lines of code as -1
'''
def GetCodeQuality(model_owner : str, model_name : str):
    full_name = model_owner + "/" + model_name # Full model name    
    info = api.model_info(full_name)
    style_guide = flake8.get_style_guide()
    fileList : list = []
    LoC = 0 # lines of code
    sibs = info.siblings # info.siblings is a list of all files in the repo, each file is a RepoSibling
    for sib in sibs:
        file = sib.rfilename
        if '.py' in file:
            # Repo Contains a pytohn file
            path = SingleFileDownload(full_name= full_name, filename= file, landingPath="C:/Users/noahb/OneDrive/Documents/SCHOOL/ECE 30861/DownloadedREADMEs")
            fileList.append(path)
            # Count number of lines in python file
            f = open(path, "r")
            length = len(f.readlines())
            LoC += length
        
    # If fileList is empty, check the base model for python files
    if fileList == []:
        base_model = info.cardData['base_model']
        full_name = base_model
        info = api.model_info(full_name) # Reset API endpoint
        sibs = info.siblings # info.siblings is a list of all files in the repo, each file is a RepoSibling
        for sib in sibs:
            file = sib.rfilename
            if '.py' in file:
                # Repo Contains a pytohn file
                path = SingleFileDownload(full_name= full_name, filename= file, landingPath="C:/Users/noahb/OneDrive/Documents/SCHOOL/ECE 30861/DownloadedREADMEs")
                fileList.append(path)
                # Count number of lines in python file
                f = open(path, "r")
                length = len(f.readlines())
                LoC += length
    
    if fileList != []:
        report = style_guide.check_files([fileList])
        errors = report.total_errors
    else:
        errors = -1
        LoC = -1
        
    return CodeQualityData(issues = errors, linesOfCode = LoC)
    
def GetPerformanceData(model_owner : str, model_name : str):
    full_name = model_owner + "/" + model_name # Full model name    
    info = api.model_info(full_name)
    model_downloads = info.downloads
    model_likes = info.likes
    return PerformanceClaimsData(likes= model_likes, downloads= model_downloads)

# Model Downloading
# This function downloads the README from the selected model repo and stores it to the cache
def SingleFileDownload(full_name : str, filename : str, landingPath : str):
    # full_name = model_owner + "/" + model_name # Full model name    
    model_path = hf_hub_download(repo_id = full_name, filename = filename, local_dir = landingPath)
    print(f"File downloaded to: {model_path}")
        
    return model_path
    

# downloads the entire model repository and stores it in the cache
def fullDownload(model_owner, model_name, landingPath):
    full_name = model_owner + "/" + model_name # Full model name    
    model_path = snapshot_download(full_name, local_dir = landingPath)

    # print(f"Model downloaded to: {model_path}")    
    return model_path







'''Artifact Model Data Fetching, kept for reference:'''
class model:
    def __init__(self, model_owner, model_name):
        self.full_name = model_owner + "/" + model_name # Full model name
        self.api = HfApi()
        
        # Get general model information
        info = self.api.model_info(self.full_name) # Contains all model information
        model_card = info.cardData  # Contains model metadata found at the beginning of the README.md for each model Note: IS A DICTIONARY
        
        # self.license = self.GetModelLicense(info)
        self.sha = info.sha
        # self.downloads = info.downloads
        # self.likes = info.likes
        self.library = info.library_name
        self.base_model = model_card['base_model']
        self.inference = info.inference
        self.siblings = info.siblings
        # self.params = self.GetParameters(info)
        self.url = RepoUrl(self.full_name)
        # self.readmePath = self.SingleFileDownload(filename="README.md")
        self.printSiblings()
    
    def printSiblings(self):
        print('Repo files for: '+self.full_name)
        for n in self.siblings:
            print(n)

  

if __name__ == "__main__":
    owner = "google"
    model_name = "gemma-3-27b-it"
    # file = "README.md"
    m = model(owner, model_name)
    # print(m.base_model)
    # GetModelInfo(model_owner=owner, model_name=model)
    # partialDownload(model_owner=owner, model_name=model, filename=file)
    
    # NO SPACE TO DOWNLOAD FULL MODEL ON ECEPROG
    # fullDownload(model_owner=owner, model_name=model)
    