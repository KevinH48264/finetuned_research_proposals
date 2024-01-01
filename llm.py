# imports
import dotenv
import os
import openai
from openai import OpenAI
import time
import json

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_GPT4_API_KEY")

# setup OpenAI API key
openai_client = OpenAI(api_key=openai.api_key)

def complete_text_openai(prompt, system_prompt="You are a helpful assistant.", stop_sequences=[], model="gpt-3.5-turbo-1106", max_tokens_to_sample=2000, temperature=0.2, log_file=None, json_required=False, tools=None, available_functions=None, **kwargs):
    # print("\nOpenAI model: ", model, "\nPrompt: ", prompt, "\nPrompt length: ", len(prompt))
    """ Call the OpenAI API to complete a prompt."""

    # Handle JSON calls or if tools are required
    if json_required and (model == "gpt-3.5-turbo-1106" or model == "gpt-4-1106-preview"):
        raw_request = {
            "model": model,
            "response_format": { "type": "json_object" },
            "temperature": temperature,
            "max_tokens": max_tokens_to_sample,
            "stop": stop_sequences or None,  # API doesn't like empty list
            **kwargs
        }
    elif tools:
        raw_request = {
            "model": model,
            "tools": tools,
            "tool_choice": "auto",
            "max_tokens": max_tokens_to_sample,
            "stop": stop_sequences or None,  # API doesn't like empty list
            "temperature": temperature,
            **kwargs
        }
    else:
        raw_request = {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens_to_sample,
            "stop": stop_sequences or None,  # API doesn't like empty list
            **kwargs
        }
    
    if model.startswith("gpt-3.5") or model.startswith("gpt-4"):
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
        response = openai_client.chat.completions.create(**{"messages": messages,**raw_request})
        # print("RESPONSE: ", response)
        completion = response.choices[0].message.content
        tool_calls = response.choices[0].message.tool_calls

        # Ensure that the completion is JSON parsable. If it isn't, ask GPT to make it JSON parsable by doubling the max tokens.
        if json_required and (model == "gpt-3.5-turbo-1106" or model == "gpt-4-1106-preview"):
            try:
                completion_json = json.loads(completion)
                print("In complete_text_openai(), Completion JSON: ", completion_json)
            except:
                print("In complete_text_openai(), COMPLETION NOT IN JSON")
                convert_to_json_prompt = f'''Close this incomplete JSON so that it's in proper JSON format: {completion}'''
                raw_request = {
                    "model": model,
                    "response_format": { "type": "json_object" },
                    "temperature": temperature,
                    "max_tokens": max_tokens_to_sample*2,
                    "stop": stop_sequences or None,  # API doesn't like empty list
                    **kwargs
                }
                messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": convert_to_json_prompt}]
                response = openai_client.chat.completions.create(**{"messages": messages,**raw_request})
                completion = response.choices[0].message.content
                # print("NEW COMPLETION: ", completion)

        if tool_calls:
            messages.append(response.choices[0].message)
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(**function_args)
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # extend conversation with function response
                print(f"Function calling required action: \nfunction_name: {function_name}, \ntool_function.arguments: {function_args}")
            # second_response = openai_client.chat.completions.create(
            #     model=model,
            #     messages=messages,
            # )  # get a new response from the model where it can see the function response
            return "Function calling complete!"
    else:
        response = openai.Completion.create(**{"prompt": prompt,**raw_request})
        completion = response["choices"][0]["text"]

    # if log_file:
    #     with open(log_file, "a", 1) as log_file:
    #         log_file.write(f"\nPrompt: {prompt}\n\nCompletion: {completion}\n")
    return completion