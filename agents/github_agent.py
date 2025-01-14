from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools.tools import get_github_data


def create_github_agent_graph():
    # Using the following: https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [get_github_data]
    graph = create_react_agent(model, tools=tools)

    return graph