from deploypilot.config import GITHUB_TOKEN
from github import Github

class GitHubClient:
    def __init__(self):
        self.client = Github(GITHUB_TOKEN)

    def get_repo_info(self, repo_name):
        """Fetch repository details."""
        try:
            repo = self.client.get_repo(repo_name)
            return {
                "name": repo.full_name,
                "description": repo.description,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "language": repo.language,
                "topics": repo.get_topics(),
            }
        except Exception as e:
            return {"error": f"Failed to fetch repo: {str(e)}"}
    
    def get_repo_structure(self, repo_name):  # ✅ NEW METHOD
        """Fetch repository file structure."""
        try:
            repo = self.client.get_repo(repo_name)
            contents = repo.get_contents("")
            structure = []
            
            while contents:
                file_content = contents.pop(0)
                structure.append(file_content.path)
                if file_content.type == "dir":
                    contents.extend(repo.get_contents(file_content.path))
            
            return structure
        except Exception as e:
            return {"error": f"Failed to fetch repo structure: {str(e)}"}
