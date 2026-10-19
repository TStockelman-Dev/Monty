import os
import argparse
import sys

from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type = str, help = "User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable not set")
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ]
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    for _ in range(20):
        try:
            response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )
            if response.usage == None:
                raise RuntimeError("Usage information not available")


            if args.verbose:
                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {response.usage.prompt_tokens}")
                print(f"Response tokens: {response.usage.completion_tokens}")

            message = response.choices[0].message
            messages.append(message)
            if not message.tool_calls:
                return message.content

            for tool_call in message.tool_calls:
                if tool_call.type != "function":
                    continue
                result_message = call_function(tool_call, args.verbose)
                messages.append(result_message)
                if not result_message.get("content"):
                    raise RuntimeError(f"Empty function response for {tool_call.function.name}")
                if args.verbose:
                    print(f"-> {result_message['content']}")
        except Exception as e:
            print(f"Error occurred: {e}")
    if message.content:
        print(f"Final response: {message.content}")
        return
    print(f"Max iterations reached")
    sys.exit(1)


if __name__ == "__main__":
    main()
