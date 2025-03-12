import openai
import os
from dotenv import load_dotenv
from deploypilot.diagram_generator import DiagramGenerator

class DeploymentGenerator:
    def __init__(self):
        """Initializes the DeploymentGenerator by loading API credentials and setting up the OpenAI client."""
        load_dotenv()  # Load environment variables from .env file

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")

        self.client = openai.OpenAI(api_key=api_key)  # ✅ Updated OpenAI client
        self.diagram_generator = DiagramGenerator()
        self.model = "gpt-3.5-turbo"
        self.temperature = 0.7

    def analyze_project_services(self, repo_name: str, project_structure: str) -> dict:
        """Analyze project structure and determine recommended cloud services."""
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
            response = self.client.chat.completions.create(  # ✅ Updated API call
                model=self.model,
                messages=[{"role": "system", "content": "You are a cloud infrastructure expert."},
                          {"role": "user", "content": prompt}],
                temperature=self.temperature
            )

            return response.choices[0].message.content  # ✅ Corrected response format
        except Exception as e:
            return {"error": f"An error occurred during service analysis: {str(e)}"}
