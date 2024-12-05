from typing import List
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class GithubProfileData(BaseModel):
    name: str | None = Field(description="Name of the GitHub user", default=None)
    avatar_url: str | None = Field(description="URL of the GitHub user's avatar", default=None)
    bio: str | None = Field(description="Bio of the GitHub user", default=None)
    public_repos: int = Field(description="Number of public repositories owned by the GitHub user")
    followers: int = Field(description="Number of followers of the GitHub user")
    following: int = Field(description="Number of users the GitHub user is following")
    top_languages: dict = Field(description="Top programming languages used by the GitHub user", default={})
    total_repos: int = Field(description="Total number of repositories owned by the GitHub user", default=0)

class ConversationStarters(BaseModel):
    language_based: List[str] = Field(description="Conversation starters based on programming languages")

conversation_starters_parser = PydanticOutputParser(pydantic_object=ConversationStarters)
github_data_parser = PydanticOutputParser(pydantic_object=GithubProfileData)