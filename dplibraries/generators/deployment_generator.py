import os
from dotenv import load_dotenv
from github import Github, ContentFile
from openai import OpenAI
from dplibraries.generators.diagram_generator import DiagramGenerator

class DeploymentGenerator:
    def __init__(self):
        """Initialize OpenAI and GitHub clients."""
        load_dotenv()

        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in .env")

        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            raise ValueError("GITHUB_TOKEN not found in .env")

        self.client = OpenAI(api_key=openai_api_key)
        self.gh = Github(github_token)
        self.diagram_generator = DiagramGenerator()

        self.model = "gpt-3.5-turbo"
        self.temperature = 0.7

    def recommend_deployment_target(self, repo_name: str, project_structure: str) -> str:
        """Use OpenAI to recommend a suitable deployment platform based on the repo."""
        prompt = f"""
        Given the following project structure for a GitHub repository named '{repo_name}', suggest the most appropriate deployment platform 
        from the following options: AWS, Firebase, Vercel, Google Cloud.

        Just respond with the most suitable platform name.

        Project Structure:
        {project_structure}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a deployment strategy expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return "unknown"

    def _get_project_structure(self, full_repo_name: str) -> str:
        """Generate a tree-like textual structure of the GitHub repository."""
        repo = self.gh.get_repo(full_repo_name)
        contents = repo.get_contents("")
        structure = []

        def traverse_dir(contents, prefix=""):
            for content in contents:
                if content.type == "dir":
                    structure.append(f"{prefix}{content.name}/")
                    try:
                        inner = repo.get_contents(content.path)
                        traverse_dir(inner, prefix + "  ")
                    except Exception:
                        continue
                else:
                    structure.append(f"{prefix}{content.name}")

        traverse_dir(contents)
        return "\n".join(structure)

    def analyze_project_services(self, repo_name: str, project_structure: str) -> dict:
        """Ask OpenAI to map files to cloud services."""
        prompt = (
            f"""Analyze the following project structure for {repo_name} and determine which cloud provider services 
            (AWS, GCP, Firebase, Vercel, etc.) should be used for each file based on its functionality.

            Provide the response in JSON format with file paths as keys and the recommended cloud services as values.

            Project Structure:
            {project_structure}
            """
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a cloud infrastructure expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return {"error": f"Service analysis failed: {str(e)}"}

    def generate_files(self, deployment_type: str, repo_name: str, repo_url: str = None, project_structure: str = None) -> dict:
        """
        Generate deployment files, analyze services, and create diagram.

        Args:
            deployment_type (str): AWS, Firebase, Vercel, etc.
            repo_name (str): Name of the repo (used in prompts)
            repo_url (str): GitHub URL, e.g. https://github.com/user/repo
            project_structure (str): (Optional) project file layout as string

        Returns:
            dict: mapping of filenames to content
        """
        prompts = {
            "AWS": f"Generate a Dockerfile and a Terraform config for deploying {repo_name} to AWS ECS.",
            "Vercel": f"Generate a vercel.json file for deploying {repo_name} (Next.js app) to Vercel.",
            "Firebase": f"Generate a firebase.json and Firestore rules for {repo_name}.",
            "Google Cloud": f"Generate Kubernetes YAML for deploying {repo_name} to GKE.",
        }

        if deployment_type not in prompts:
            return {"error.txt": f"No template available for {deployment_type}"}

        try:
            # Auto-generate project structure if not provided
            if not project_structure and repo_url:
                parts = repo_url.rstrip("/").split("/")[-2:]
                full_repo_name = "/".join(parts)
                project_structure = self._get_project_structure(full_repo_name)

            service_mapping = self.analyze_project_services(repo_name, project_structure)
            architecture_diagram = self.diagram_generator.generate_architecture_diagram(repo_name, project_structure)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a DevOps expert."},
                    {"role": "user", "content": prompts[deployment_type]}
                ],
                temperature=self.temperature
            )

            output = response.choices[0].message.content

            file_mappings = {
                "AWS": {"Dockerfile": output.split("\n\n")[0], "terraform.tf": output.split("\n\n")[1]},
                "Vercel": {"vercel.json": output},
                "Firebase": {"firebase.json": output},
                "Google Cloud": {"deployment.yaml": output},
            }

            final_output = file_mappings[deployment_type]
            final_output["service_mapping.json"] = service_mapping
            final_output["architecture_diagram.mmd"] = architecture_diagram
            return final_output

        except Exception as e:
            return {"error.txt": f"An error occurred: {str(e)}"}


def generate_deployment_files(repo_url: str, target_platform: str = None) -> dict:
    """
    High-level wrapper for the LangChain agent to get deployment suggestions + files.
    """
    dg = DeploymentGenerator()

    # Extract repo name (e.g., "user/repo") from URL
    parts = repo_url.rstrip("/").split("/")[-2:]
    repo_name = parts[-1]
    full_repo_name = "/".join(parts)

    # Get project structure
    project_structure = dg._get_project_structure(full_repo_name)

    # Recommend platform if not provided
    if not target_platform:
        target_platform = dg.recommend_deployment_target(repo_name, project_structure)

    # Generate deployment files
    files = dg.generate_files(target_platform, repo_name, repo_url, project_structure)

    return {
        "recommendation": target_platform,
        "files": files
    }
