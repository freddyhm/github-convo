from typing import Dict
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from output_parsers import conversation_starters_parser, ConversationStarters
from agents.github_agent import generate_github_info

load_dotenv()

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
    
    formatted_result = generate_github_info(username)    

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
