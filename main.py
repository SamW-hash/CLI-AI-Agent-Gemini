import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("api_key not found: check your .env")
client = genai.Client(api_key=api_key)
parser = argparse.ArgumentParser(description="Agent")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
response = client.models.generate_content(model="gemini-2.5-flash", contents=messages)

if response.usage_metadata.candidates_token_count == None:
    raise RuntimeError("usage_metadata not available: likely failed API request")
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
print(response.text)