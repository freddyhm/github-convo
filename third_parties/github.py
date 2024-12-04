from typing import Dict, List
from github import Github
from github.Repository import Repository
from collections import Counter
import os
from langchain_core.tools import Tool
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from output_parsers import conversation_starters_parser, github_data_parser, ConversationStarters

load_dotenv()

def extract_contribution_data(github_user):
    languages_count = Counter()
    
    try:
        repos: List[Repository] = list(github_user.get_repos())
    
        for repo in repos:
            if not repo.fork:
                if repo.language:
                    languages_count[repo.language] += 1
    except Exception as error:
        print(f"Error fetching repositories: {str(error)}")
        repos = []
    
    contribution_data = {
        "total_repos": len(repos),
        "top_languages": dict(languages_count.most_common(5))
    }
    return contribution_data


def get_github_data(username: str) -> Dict:
    try:
        github_user = Github(os.getenv("GITHUB_ACCESS_TOKEN")).get_user(username)
        
        if github_user.login :
            profile_data = {
                "name": github_user.name or username,
                "avatar_url": github_user.avatar_url,
                "bio": github_user.bio or "",
                "public_repos": github_user.public_repos,
                "followers": github_user.followers,
                "following": github_user.following
            }
            
            return {
                "profile": profile_data,
                "contributions": extract_contribution_data(github_user)
            }
            
    except Exception as error:
        print(f"GitHub API Error: {str(error)}")
        raise Exception(f"Failed to fetch GitHub data: {str(error)}")

def get_github_data2(llm, username: str):
    template2 = """Given the username {name}, retrieve their Github data and return it in the following JSON format without any markdown formatting or code blocks. The output should be a raw JSON object.
                    
                {format_instructions}

                Remember: Return ONLY the JSON object without any additional text, markdown formatting, or code blocks."""

    prompt_template2 = PromptTemplate(
        template=template2, input_variables=["name"],
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
        input={"input": prompt_template2.format_prompt(name="freddyhm")}
    )
    formatted_result = github_data_parser.parse(agent_result["output"])
    
    return formatted_result
    

def generate_conversation_starters(username: str) -> Dict:

    template = """
    Given the following information about a GitHub user, generate engaging conversation starters.
    Make them personal, specific, and related to their actual work and interests.
    
    GitHub Profile:
    Name: {name}
    Bio: {bio}
    Public Repositories: {repos}
    Followers: {followers}
    Following: {following}
    
    Top Programming Languages: {languages}
    Total Repositories: {total_repos}
    
    Generate language-based conversation starters that focus on their programming language preferences and experience.
    
    {format_instructions}
    """

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["name", "bio", "repos", "followers", "following", "languages", "total_repos"],
        partial_variables={"format_instructions": conversation_starters_parser.get_format_instructions()}
    )
    
    formatted_result = get_github_data2(llm, username)    

    chain = prompt | llm | conversation_starters_parser
    
    final_result: ConversationStarters = chain.invoke({
        "name": formatted_result.name,
        "bio": formatted_result.bio,
        "repos": formatted_result.public_repos,
        "followers": formatted_result.followers,
        "following": formatted_result.following,
        "languages": ", ".join(formatted_result.top_languages.keys()),
        "total_repos": formatted_result.total_repos
    })

    return {
        "profile": {
            "name": formatted_result.name,
            "avatar_url": formatted_result.avatar_url,
            "bio": formatted_result.bio,
            "public_repos": formatted_result.public_repos,
            "followers": formatted_result.followers,
            "following": formatted_result.following
        },
        "contributions": {
            "total_repos": formatted_result.total_repos,
            "top_languages": formatted_result.top_languages
        },
        "language_based": final_result.language_based
    }
