from langchain.prompts import PromptTemplate
from langchain.agents import Tool, create_react_agent, AgentExecutor
from langchain import hub
from output_parsers import github_data_parser
from tools.tools import get_github_data

def generate_github_info(llm, username: str):
    template = """Given the username {name}, retrieve their Github data and return it in the following JSON format without any markdown formatting or code blocks. The output should be a raw JSON object.
                    
                {format_instructions}

                Remember: Return ONLY the JSON object without any additional text, markdown formatting, or code blocks."""

    prompt_template = PromptTemplate(
        template=template, input_variables=["name"],
        partial_variables={"format_instructions": github_data_parser.get_format_instructions()}
    )
    
    tools_for_agent = [
        Tool(
            name="Get data from GitHub",
            func=get_github_data,
            description="useful for when you need to get Github data",  # super important - concise and has enough info
        )
    ]

    react_prompt = hub.pull(
        "hwchase17/react"
    )
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(
        agent=agent, tools=tools_for_agent, verbose=True
    )
    agent_result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name=username)}
    )
    formatted_result = github_data_parser.parse(agent_result["output"])
    
    return formatted_result
