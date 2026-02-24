from huggingface_hub import InferenceClient
import os
from dotenv import dotenv_values
from pathlib import Path

# Load .env from project root using absolute paths
# __file__ = /utils/llm.py, so parent is /utils, parent.parent is /ai_study
llm_file = Path(__file__).resolve()  # Absolute path to llm.py
project_root = llm_file.parent.parent  # Go up to ai_study directory
env_path = project_root / ".env"

if env_path.exists():
    env_vars = dotenv_values(dotenv_path=env_path)
    for key, value in env_vars.items():
        os.environ[key] = value

API_KEY = os.getenv("HUGGINGFACE_API_KEY")  # Match the variable name in .env

if not API_KEY:
    raise ValueError("HUGGINGFACE_API_KEY not found in environment variables")

client = InferenceClient(api_key=API_KEY, timeout=120)

def query_model(system_prompt, user_input, max_tokens=800):
    """
    Query the LLM with system and user prompts.
    
    Args:
        system_prompt (str): System prompt for context and instruction
        user_input (str): User's input/query
        max_tokens (int): Maximum tokens for response (default 800)
    
    Returns:
        str: Model response or error message
    """
    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        
        response = client.chat_completion(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=messages,
            temperature=0.7,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"