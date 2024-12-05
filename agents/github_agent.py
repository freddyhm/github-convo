from langchain.prompts import PromptTemplate
from langchain.agents import Tool, create_react_agent, AgentExecutor
from langchain_core.messages import ToolMessage
from langchain import hub
from langchain_openai import ChatOpenAI
from output_parsers import github_data_parser
from tools.tools import get_github_data

def generate_github_info(username: str):

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini").bind_tools([get_github_data])

    template = """Given the username {name}, retrieve their Github data and return it in the following JSON format without any markdown formatting or code blocks. The output should be a raw JSON object.
                    
                {format_instructions}

                Remember: Return ONLY the JSON object without any additional text, markdown formatting, or code blocks."""

    prompt_template = PromptTemplate(
        template=template, input_variables=["name"],
        partial_variables={"format_instructions": github_data_parser.get_format_instructions()}
    )
    
    agent_result = llm.invoke(prompt_template.format_prompt(name=username))
    selected_tool = {"get_github_data": get_github_data}[agent_result.tool_calls[0]["name"].lower()]
    tool_output = selected_tool.invoke(agent_result.tool_calls[0]["args"])

    formatted_result = github_data_parser.parse(str(tool_output.get("profile")).replace("'", '"'))
    
    return formatted_result
