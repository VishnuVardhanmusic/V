# src/review_agent.py

import requests
from config import BASE_URL, API_KEY, MODEL_NAME

def getReviewFromLLM(codeSnippet: str, guidelineDescription: str) -> dict:
    """
    Sends code and guideline to Claude 3.5 via LiteLLM proxy and returns JSON review.

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

Reply strictly in JSON with the following keys:
- is_violation (true or false)
- reasoning
- suggestion
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    try:
        response = requests.post(f"{BASE_URL}/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]

        return eval(content) if content.strip().startswith("{") else {
            "is_violation": None,
            "reasoning": "Unexpected response format",
            "suggestion": content.strip()
        }

    except Exception as e:
        return {
            "is_violation": None,
            "reasoning": f"Request Error: {str(e)}",
            "suggestion": "N/A"
        }
