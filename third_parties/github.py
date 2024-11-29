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

def get_github_data(username: str) -> Dict:
    """
    Retrieve GitHub user data including languages, contributions, and interests
    """
    try:
        g = Github(os.getenv("GITHUB_ACCESS_TOKEN"))
        user = g.get_user(username)
        
        # Test if we can access the user (validates token and username)
        _ = user.login
        
        # Get basic profile info
        profile_data = {
            "name": user.name or username,
            "avatar_url": user.avatar_url,
            "bio": user.bio or "",
            "public_repos": user.public_repos,
            "followers": user.followers,
            "following": user.following
        }
        
        # Get languages and repositories
        languages_count = Counter()
        starred_topics = Counter()
        
        try:
            repos: List[Repository] = list(user.get_repos())
            
            for repo in repos:
                if not repo.fork:  # Only count original repos, not forks
                    if repo.language:
                        languages_count[repo.language] += 1
                    try:
                        for topic in repo.get_topics():
                            starred_topics[topic] += 1
                    except Exception:
                        continue  # Skip if topics can't be fetched
        except Exception as e:
            print(f"Error fetching repositories: {str(e)}")
            repos = []
        
        # Get contribution patterns
        contribution_data = {
            "total_repos": len(repos),
            "top_languages": dict(languages_count.most_common(5)),
            "top_topics": dict(starred_topics.most_common(5))
        }
        
        return {
            "profile": profile_data,
            "contributions": contribution_data
        }
        
    except Exception as e:
        print(f"GitHub API Error: {str(e)}")
        raise Exception(f"Failed to fetch GitHub data: {str(e)}")

def generate_conversation_starters(github_data: Dict) -> Dict:
    """
    Generate conversation starters based on GitHub profile data using LangChain
    """
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
    Top Repository Topics: {topics}
    Total Repositories: {total_repos}
    
    Generate three types of conversation starters:
    1. Language-based: Focus on their programming language preferences and experience
    2. Topic-based: Related to their repository topics and interests
    3. General: About their GitHub activity and community involvement
    
    {format_instructions}
    """
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["name", "bio", "repos", "followers", "following", "languages", "topics", "total_repos"],
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
        "topics": ", ".join(github_data["contributions"]["top_topics"].keys()),
        "total_repos": github_data["contributions"]["total_repos"]
    })
    
    return {
        "language_based": result.language_based,
        "topic_based": result.topic_based,
        "general": result.general
    }
