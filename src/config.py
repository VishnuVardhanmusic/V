import os
MODEL_NAME = "anthropic.claude-3-5-sonnet-20241022.v2:0"
BASE_URL = os.getenv("LITELLM_URL", "https://litellm-api.up.railway.app/")
API_KEY = os.getenv("LITELLM_API_KEY", "<your_api_key_here>")
