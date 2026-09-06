from functools import lru_cache

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from config import (
    PARAMETERS,
    GROQ_API_KEY,
    LLAMA_MODEL_ID,
    GRANITE_MODEL_ID,
    MISTRAL_MODEL_ID,
)


# ---------------------------------------------------------
# JSON output structure
# ---------------------------------------------------------

class AIResponse(BaseModel):
    summary: str = Field(
        description="Summary of the user's message"
    )

    sentiment: int = Field(
        description="Sentiment score from 0 (negative) to 100 (positive)"
    )

    response: str = Field(
        description="Suggested response to the user"
    )


# ---------------------------------------------------------
# JSON parser
# ---------------------------------------------------------

json_parser = JsonOutputParser(
    pydantic_object=AIResponse
)


# ---------------------------------------------------------
# Initialize Groq model
# ---------------------------------------------------------

@lru_cache(maxsize=None)
def initialize_model(model_id):
    """Create and cache a Groq chat model."""

    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is not set. "
            "Add your Groq API key to the .env file."
        )

    return ChatGroq(
        model=model_id,
        temperature=PARAMETERS["temperature"],
        max_tokens=PARAMETERS["max_tokens"],
        groq_api_key=GROQ_API_KEY,
    )


# ---------------------------------------------------------
# Prompt template
# ---------------------------------------------------------

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an AI assistant helping with customer inquiries.

Analyze the user's message and return a JSON response.

{format_prompt}

The sentiment must be an integer between 0 and 100:
- 0 = extremely negative
- 50 = neutral
- 100 = extremely positive
"""
        ),
        (
            "human",
            "{user_prompt}"
        ),
    ]
)


# ---------------------------------------------------------
# Generate response
# ---------------------------------------------------------

def get_ai_response(model, system_prompt, user_prompt):

    chain = (
        prompt_template
        | model
        | json_parser
    )

    return chain.invoke(
        {
            "format_prompt": json_parser.get_format_instructions(),
            "user_prompt": user_prompt,
        }
    )


# ---------------------------------------------------------
# Model-specific functions
# ---------------------------------------------------------

def llama_response(system_prompt, user_prompt):
    model = initialize_model(LLAMA_MODEL_ID)

    return get_ai_response(
        model,
        system_prompt,
        user_prompt
    )


def granite_response(system_prompt, user_prompt):
    model = initialize_model(GRANITE_MODEL_ID)

    return get_ai_response(
        model,
        system_prompt,
        user_prompt
    )


def mistral_response(system_prompt, user_prompt):
    model = initialize_model(MISTRAL_MODEL_ID)

    return get_ai_response(
        model,
        system_prompt,
        user_prompt
    )