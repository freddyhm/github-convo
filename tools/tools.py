from typing import Dict, List
from collections import Counter
import os
from github import Github
from github.Repository import Repository

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
        
        if github_user.login:
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
