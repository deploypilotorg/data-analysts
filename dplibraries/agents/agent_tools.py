from langchain.tools import tool
from dplibraries.generators.deployment_generator import generate_deployment_files
from dplibraries.generators.diagram_generator import generate_architecture_diagram

@tool
def recommend_deployment(repo_url: str) -> str:
    """Given a GitHub repo URL, recommend the best deployment platform."""
    result = generate_deployment_files(repo_url, target_platform=None)
    return result.get('recommendation', 'No recommendation available.')

@tool
def get_deployment_files(repo_url: str) -> str:
    """Given a GitHub repo URL, generate deployment config files (e.g., vercel.json, service mapping)."""
    result = generate_deployment_files(repo_url, target_platform=None)
    return result.get('files', {})

@tool
def get_architecture_diagram(repo_url: str) -> str:
    """Given a GitHub repo URL, generate a system architecture Mermaid.js diagram."""
    return generate_architecture_diagram(repo_url)

tools = [recommend_deployment, get_deployment_files, get_architecture_diagram]
