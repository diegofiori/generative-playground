import json
import os
import time
from typing import List

import openai
from openai.types.beta.threads import ThreadMessage

from agent.excecutor import FunctionExecutor
from agent.prompts import BASE_INSTRUCTION, STATUS_UPDATE
from agent.tools.github_tools import get_tools, GitHubInterface

from dotenv import load_dotenv
load_dotenv()

client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def build_frontend_developer_agent():
    tools = get_tools()
    tools.append({"type": "code_interpreter"})
    assistant = client.beta.assistants.create(
        name="Serhii, the Frontend Developer",
        instructions=BASE_INSTRUCTION,
        tools=tools,
        model="gpt-4-1106-preview"
    )
    return assistant


def get_frontend_developer_agent():
    assistants = client.beta.assistants.list()
    for assistant in assistants:
        if assistant.name == "Serhii, the Frontend Developer":
            return assistant
    return build_frontend_developer_agent()


class FrontendAgentRunner:
    def __init__(self):
        self.agent = get_frontend_developer_agent()
        github_interface = GitHubInterface.from_github_token(
            os.environ["GITHUB_TOKEN"], 
            repository=os.environ["GITHUB_REPOSITORY"]
        )
        self.executor = FunctionExecutor([github_interface])
        self.thread = client.beta.threads.create()
    
    def run(self, text: str) -> List[ThreadMessage]:
        message = client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=text
        )
        run = client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.agent.id,
            instructions=STATUS_UPDATE.template.format(
                status=self.executor.execute("getStatus")
            ),
        )
        while run.status != "completed":
            if run.status == "requires_action":
                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                tool_outputs = []
                for tool_call in tool_calls:
                    run_output = self.executor.execute(
                        tool_call.function.name, 
                        **json.loads(tool_call.function.arguments)
                    )
                    tool_outputs.append(
                        {
                            "tool_call_id": tool_call.id,
                            "output": run_output if isinstance(run_output, str) else json.dumps(run_output)
                        }
                    )
                run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=self.thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )  
            elif run.status == "failed":
                raise Exception(run.last_error.message) 
            else:
                time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id
            )
        messages = client.beta.threads.messages.list(
            thread_id=self.thread.id
        )
        return list(messages)
