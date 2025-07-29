# 📦 Python Setup Guide for Project Dependencies


This guide will help you install all required packages and system dependencies needed to run this Python project.


# ✅ Prerequisites

- Python is already installed

- Internet access for downloading packages

 # 1. Clone the Repository
### Create a LocalRepo Folder
```bash 
mkdir LocalRepo
```
### Then, open the folder
```bash
cd LocalRepo
```
### Clone the GitHub repository
```bash 
git clone git@github.com:jmignacio05/Food-Rescue-and-Redistibution-Platform.git
```

 # 2. Create a Virtual Environment

```bash

python -m venv env 
```
### Activate your virtual environment
```bash
source env/bin/activate  
```
# 3. Install dependencies
```bash
pip install flet pymongo requests matplotlib uvicorn fastapi
```
```bash
sudo apt-get -y install libmpv1
```



 # 4. To Run the App

## Open the cloned GitHub repository
```bash
cd LocalRepo/Food-Rescue-and-Redistibution-Platform
```

## Run the app 
```bash
python food_rescue_platform/main.py
```


## Team Members 
### Fernandez, Bryan Frederick T. (Frontend Developer and UI/UX Designer)
### Ignacio, Joaquin Miguel G. (Project Manager)
### Maliwat, Laurenz Kyle A. (Documentation Specialist)
