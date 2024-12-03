from typing import Dict, List
from github import Github
from github.Repository import Repository
from collections import Counter
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from output_parsers import conversation_starters_parser, ConversationStarters

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

def generate_conversation_starters(github_data: Dict) -> Dict:
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
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["name", "bio", "repos", "followers", "following", "languages", "total_repos"],
        partial_variables={"format_instructions": conversation_starters_parser.get_format_instructions()}
    )
    
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    
    chain = prompt | llm | conversation_starters_parser
    
    result: ConversationStarters = chain.invoke({
        "name": github_data["profile"]["name"],
        "bio": github_data["profile"]["bio"],
        "repos": github_data["profile"]["public_repos"],
        "followers": github_data["profile"]["followers"],
        "following": github_data["profile"]["following"],
        "languages": ", ".join(github_data["contributions"]["top_languages"].keys()),
        "total_repos": github_data["contributions"]["total_repos"]
    })
    
    return {
        "language_based": result.language_based
    }
