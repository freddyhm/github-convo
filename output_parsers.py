from typing import List
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class ConversationStarters(BaseModel):
    language_based: List[str] = Field(description="Conversation starters based on programming languages")

conversation_starters_parser = PydanticOutputParser(pydantic_object=ConversationStarters)
