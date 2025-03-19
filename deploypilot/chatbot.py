import openai
from deploypilot.config import OPENAI_API_KEY
from deploypilot.github_client import GitHubClient
from deploypilot.repo_visualizer import RepoVisualizer  # ✅ NEW IMPORT

class ChatBot:
    def __init__(self):
        self.github_client = GitHubClient()
        self.repo_visualizer = RepoVisualizer()  # ✅ NEW INSTANCE
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)

    def generate_response(self, user_input):
        """Handles user queries about GitHub repositories."""
        if "repo info" in user_input.lower():
            repo_name = user_input.split()[-1]
            repo_data = self.github_client.get_repo_info(repo_name)
            return f"Repo Info: {repo_data}"
        
        elif "visualize repo" in user_input.lower():  # ✅ NEW FEATURE
            repo_name = user_input.split()[-1]
            diagram = self.repo_visualizer.generate_repo_diagram(repo_name)
            return f"Mermaid.js Diagram:\n```mermaid\n{diagram}\n```"
        
        else:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": user_input}]
                )
                return response.choices[0].message.content
            except Exception as e:
                return f"Error: {str(e)}"

if __name__ == "__main__":
    bot = ChatBot()
    while True:
        user_input = input("Ask something: ")
        if user_input.lower() == "exit":
            break
        print("\n🤖:", bot.generate_response(user_input))