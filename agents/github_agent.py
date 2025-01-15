from langchain_openai import ChatOpenAI
from openai import OpenAI
from tools.tools import get_github_data
import json


def get_outputs_for_tool_call(tool_call):
    username = json.loads(tool_call.function.arguments)["username"]
    github_data = get_github_data(username)
    return {
        "tool_call_id": tool_call.id,
        "output": json.dumps(github_data)
    }


def create_github_agent(instructions):

    client = OpenAI()
    assistant = client.beta.assistants.create(
        name="Github Assistant",
        instructions="You are a Github API assistant that can retrieve Github data for a given username",
        tools=[{"type": "function", "function": {
            "name": "get_github_data",
            "description": "Get Github data for a given username",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {"type": "string"}
                }
            }
        }}],
        model="gpt-4o-mini",
    )


    thread = client.beta.threads.create()

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=instructions
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
        thread_id=thread.id
        )
        print(messages)
    else:
        print(run.status)


    tool_calls = run.required_action.submit_tool_outputs.tool_calls
    tool_outputs = map(get_outputs_for_tool_call, tool_calls)
    tool_outputs = list(tool_outputs)

    if tool_outputs:
        try:
            run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
            print("Tool outputs submitted successfully.")
        except Exception as e:
            print("Failed to submit tool outputs:", e)
        else:
            print("No tool outputs to submit.")

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
        thread_id=thread.id
        )
        print(messages)
    else:
        print(run.status)


    return messages.data[0].content[0].text.value