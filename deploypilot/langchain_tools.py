from langchain.tools import tool
from deploypilot.github_client import GitHubClient
from deploypilot.repo_visualizer import RepoVisualizer
from deploypilot.deployment_generator import DeploymentGenerator

github_client = GitHubClient()
repo_visualizer = RepoVisualizer()
deployment_generator = DeploymentGenerator()

@tool
def get_repo_info(repo_name: str) -> dict:
    """Fetch GitHub repository details such as name, stars, forks, and language."""
    return github_client.get_repo_info(repo_name)

@tool
def get_repo_structure(repo_name: str) -> list:
    """Fetch the repository file structure."""
    return github_client.get_repo_structure(repo_name)

@tool
def generate_repo_diagram(repo_name: str) -> str:
    """Generate a Mermaid.js visualization of the repository structure."""
    return repo_visualizer.generate_repo_diagram(repo_name)

@tool
def analyze_project_services(repo_name: str, project_structure: str) -> dict:
    """Analyze project files and suggest the best cloud services for deployment."""
    return deployment_generator.analyze_project_services(repo_name, project_structure)
