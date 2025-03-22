from github import Github
import os
from dotenv import load_dotenv

load_dotenv()

def get_github_client():
    token = os.getenv("GITHUB_TOKEN")
    if token is None:
        raise ValueError("GITHUB_TOKEN not found in environment variables")
        
    return Github(token)