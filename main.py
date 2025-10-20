import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

#functions ai will use
from functions.function_calling_declaration import *
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

from config import WORKING_DIR
import sys
import argparse


def call_function(function_call_part, verbose=False):
    string2func = {
        "get_file_content" : get_file_content,
        "get_files_info" : get_files_info,
        "write_file" : write_file,
        "run_python_file" : run_python_file,
    }
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")


    if function_call_part.name in string2func:
        result = string2func[function_call_part.name](WORKING_DIR, **function_call_part.args)
        return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=function_call_part.name,
                            response={"result": result},
                        )
                    ],
                )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    

def main():
    load_dotenv()
    #api
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    #arg parser
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="prompt the ai agent",type=str)
    parser.add_argument("-v","--verbose", help="increase output verbosity",action="store_true")
    args = parser.parse_args()
    prompt = args.prompt


    ###AI agent section

    #definitions
    system_prompt = """
                    You are a helpful AI coding agent.

                    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

                    - List files and directories
                    - Read file contents
                    - Execute Python files with optional arguments
                    - Write or overwrite files

                    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
                    """

    available_functions = types.Tool(
            function_declarations=[
                schema_get_files_info,
                schema_get_file_content,
                schema_write_file,
                schema_run_python_file,
            ]
        )

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]


    #AI Agent loop
    
    #call model
    response = client.models.generate_content(
        model ="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt))

    #save reponse to the message list
    for candidate in response.candidates:
        messages.append(candidate.content)


    #output
    if args.verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if response.function_calls:
        content = call_function(response.function_calls[0],args.verbose)
        if content.parts[0].function_response.response:
            if args.verbose:
                print(f"-> {content.parts[0].function_response.response}")

        else:
            raise Exception(f"error in calling function {response.function_calls[0].name}")
        

    else:
        print(response.text)








main()