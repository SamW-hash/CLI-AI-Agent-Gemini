import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import *

load_dotenv()
#set key in .env
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("api_key not found: check your .env")
client = genai.Client(api_key=api_key)
parser = argparse.ArgumentParser(description="Agent")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
response = client.models.generate_content(model="gemini-2.5-flash", contents=messages, config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt))

if response.usage_metadata.candidates_token_count == None:
    raise RuntimeError("usage_metadata not available: likely failed API request")
if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
if response.function_calls:
    for call in response.function_calls:
        function_call_result = call_function(call)
        if function_call_result.parts == []:
            raise Exception("Error1")
        if function_call_result.parts[0].function_response == None:
            raise Exception("Error2")
        if function_call_result.parts[0].function_response.response == None:
            raise Exception("Error3")
        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_results = []
        function_results.append(function_call_result.parts[0].function_response)
else: print(response.text)