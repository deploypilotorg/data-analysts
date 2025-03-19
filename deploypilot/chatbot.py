import os
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from deploypilot.langchain_tools import get_repo_info, get_repo_structure, generate_repo_diagram, analyze_project_services
from deploypilot.config import OPENAI_API_KEY

class ChatBot:
    def __init__(self):
        """Initialize chatbot with LangChain agent and tools."""
        self.llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.7, api_key=OPENAI_API_KEY)
        self.agent = initialize_agent(
            tools=[get_repo_info, get_repo_structure, generate_repo_diagram, analyze_project_services],
            llm=self.llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True  # Debugging purposes
        )

    def generate_response(self, user_input):
        """Handles user queries with LangChain's function calling."""
        return self.agent.run(user_input)

if __name__ == "__main__":
    bot = ChatBot()
    while True:
        user_input = input("Ask something: ")
        if user_input.lower() == "exit":
            break
        print("\n🤖:", bot.generate_response(user_input))
