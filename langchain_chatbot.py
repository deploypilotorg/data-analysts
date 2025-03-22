from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI

from dplibraries.agents.agent_tools import tools


def main():
    llm = ChatOpenAI(temperature=0)
    
    agent = initialize_agent(
        tools,
        llm,
        agent="chat-zero-shot-react-description",
        verbose=True,
        handle_parsing_errors=True
    )

    print("🤖 DeployPilot Chatbot is live! Ask your deployment questions.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("👋 Goodbye!")
            break
        response = agent.run(user_input)
        print("DeployPilot:", response)

if __name__ == "__main__":
    main()
