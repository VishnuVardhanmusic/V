# src/review_agent.py

from langchain.chat_models import ChatLiteLLM
from langchain.schema import HumanMessage
from config import MODEL_NAME, BASE_URL, API_KEY

import os

# Set up LiteLLM environment variables
os.environ["LITELLM_API_KEY"] = API_KEY
os.environ["LITELLM_URL"] = BASE_URL

# Initialize Claude via LiteLLM
llm = ChatLiteLLM(
    model=MODEL_NAME,
    base_url=BASE_URL
)

def getReviewFromLLM(codeSnippet: str, guidelineDescription: str) -> dict:
    """
    Sends code and guideline to Claude and returns review feedback.

    Args:
        codeSnippet (str): The flagged code line
        guidelineDescription (str): Description of the violated guideline

    Returns:
        dict: LLM response with is_violation, reasoning, suggestion
    """
    prompt = f"""
You are a strict embedded software code reviewer.

Evaluate the following C code snippet against the given guideline.

Guideline:
{guidelineDescription}

Code:
{codeSnippet}

Reply in JSON format with the following fields:
- is_violation: true or false
- reasoning: explanation of whether it's a violation or not
- suggestion: how to fix or improve it
"""
    try:
        response = llm([HumanMessage(content=prompt)])
        return eval(response.content)  # Expecting JSON dict as response
    except Exception as e:
        return {
            "is_violation": None,
            "reasoning": f"LLM Error: {str(e)}",
            "suggestion": "N/A"
        }
