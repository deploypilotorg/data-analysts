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
        self.model = "gpt-3.5-turbo"
        self.temperature = 0.7
        self.response_format = "text"

    def generate_files(self, deployment_type: str, repo_name: str) -> dict:
        """
        Generate deployment configuration files using ChatGPT.

        Args:
            deployment_type (str): The predicted deployment platform (e.g., AWS, Vercel, Firebase).
            repo_name (str): The name of the repository.

        Returns:
            dict: A dictionary with file names as keys and file contents as values.
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

            return file_mappings.get(deployment_type, {"error.txt": "File generation failed."})

        except Exception as e:
            return {"error.txt": f"An error occurred during file generation: {str(e)}"}
