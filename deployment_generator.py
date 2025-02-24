import openai
import os
from dotenv import load_dotenv

class DeploymentGenerator:
    def __init__(self):
        """
        Initializes the DeploymentGenerator by loading API credentials
        and setting up the OpenAI client.
        """
        # Load environment variables from .env file
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")

        self.client = openai.OpenAI(api_key=api_key)

        # Default configuration
        self.model = "gpt-3.5 turbo"
        self.temperature = 0.7
        self.response_format = "text"

    def analyze_project_services(self, repo_name: str, project_structure: str) -> dict:
        """
        Analyze the project structure and determine which cloud services
        should be used for each functionality.

        Args:
            repo_name (str): The name of the repository.
            project_structure (str): A textual representation of the project structure.

        Returns:
            dict: A dictionary mapping files to cloud services.
        """
        prompt = (
            f"""Analyze the following project structure for {repo_name} and determine which cloud provider services 
            (AWS, GCP, Firebase, Vercel, etc.) should be used for each file based on its functionality.
            
            Provide the response in JSON format with file paths as keys and the recommended cloud services as values.
            
            Example:
            {{
                "database/models.py": "AWS RDS",
                "authentication/login.py": "Firebase Auth",
                "server/api.py": "Google Cloud Functions"
            }}
            
            Project Structure:
            {project_structure}
            """
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a cloud infrastructure expert. Map project files to cloud services."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                response_format={"type": "json_object"}
            )

            return response.choices[0].message.content
        
        except Exception as e:
            return {"error": f"An error occurred during service analysis: {str(e)}"}

    def generate_files(self, deployment_type: str, repo_name: str, project_structure: str) -> dict:
        """
        Generate deployment configuration files and analyze cloud service requirements.

        Args:
            deployment_type (str): The predicted deployment platform (e.g., AWS, Vercel, Firebase).
            repo_name (str): The name of the repository.
            project_structure (str): A textual representation of the project structure.

        Returns:
            dict: A dictionary with file names as keys and file contents as values, including service mapping.
        """
        # Define structured prompts based on deployment type
        prompts = {
            "AWS": f"Generate a Dockerfile and a Terraform configuration for deploying {repo_name} to AWS ECS. Assume a Python app with PostgreSQL.",
            "Vercel": f"Generate a vercel.json file for deploying {repo_name} (Next.js app) to Vercel.",
            "Firebase": f"Generate a firebase.json file and Firestore rules for {repo_name}.",
            "Google Cloud": f"Generate a Kubernetes YAML configuration for deploying {repo_name} to Google Kubernetes Engine.",
        }

        if deployment_type not in prompts:
            return {"error.txt": f"No template available for {deployment_type}"}

        try:
            # First, analyze the project services
            service_mapping = self.analyze_project_services(repo_name, project_structure)

            # Generate deployment configurations
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a DevOps expert. Generate deployment configurations as accurately as possible."},
                    {"role": "user", "content": prompts[deployment_type]}
                ],
                temperature=self.temperature
            )

            generated_text = response.choices[0].message.content

            # Process the generated output into structured files
            file_mappings = {
                "AWS": {"Dockerfile": generated_text.split("\n\n")[0], "terraform.tf": generated_text.split("\n\n")[1]},
                "Vercel": {"vercel.json": generated_text},
                "Firebase": {"firebase.json": generated_text},
                "Google Cloud": {"deployment.yaml": generated_text},
            }

            # Include service mapping in the final output
            file_mappings["service_mapping.json"] = service_mapping
            return file_mappings

        except Exception as e:
            return {"error.txt": f"An error occurred during file generation: {str(e)}"}
