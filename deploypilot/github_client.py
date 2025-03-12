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
