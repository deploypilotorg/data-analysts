import openai
from deploypilot.config import OPENAI_API_KEY
from deploypilot.github_client import GitHubClient

class ChatBot:
    def __init__(self):
        self.github_client = GitHubClient()
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)  # ✅ New OpenAI client format

    def generate_response(self, user_input):
        """Handles user queries about GitHub repositories."""
        if "repo info" in user_input.lower():
            repo_name = user_input.split()[-1]  # Example input: "repo info octocat/Hello-World"
            repo_data = self.github_client.get_repo_info(repo_name)
            return f"Repo Info: {repo_data}"

        else:
            try:
                response = self.client.chat.completions.create(  # ✅ New API call
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": user_input}]
                )
                return response.choices[0].message.content  # ✅ Corrected response format
            except Exception as e:
                return f"Error: {str(e)}"  # ✅ Handles API errors gracefully

if __name__ == "__main__":
    bot = ChatBot()
    while True:
        user_input = input("Ask something: ")
        if user_input.lower() == "exit":
            break
        print("🤖:", bot.generate_response(user_input))
