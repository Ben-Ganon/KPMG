import os
from openai import AzureOpenAI
import json
from dotenv import load_dotenv, find_dotenv
from utils import json_sys_prompt, str_sys_prompt, chat_prompt_template
load_dotenv(find_dotenv())

endpoint = "https://oai-lab-test-eastus-001.openai.azure.com/"

key = os.environ.get("OAI_KEY")

deployment = "gpt-4o"

class OAI_Azure:
    def __init__(self):
        self.client =  AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=key,
        api_version="2024-05-01-preview",
    )

    def _get_completion_base(self, **kwargs) -> str:
        """
        reusable basic completion function
        :param kwargs: basically messages with/without a desired response format in the case of json output
        :return:
        """
        try:
            completion = self.client.chat.completions.create(
                model=deployment,
                messages=kwargs["messages"],
                max_tokens=800,
                temperature=0.8,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None,
                stream=False,
                response_format=kwargs.get("response_format", None)
            )
        except Exception as e:
            raise Exception("Error in completion" + str(e))
        output = completion.choices[0].message.content
        # attempt to parse the output str as a json object
        return output

    def get_completion_str(self, query: str) -> str:
        """
        (for part 1)
        standard completion for a single query with no conversation history
        :param query: user query
        :return: assistant response
        """
        messages = chat_prompt_template.copy()
        messages[0]["content"][0]["text"] = str_sys_prompt
        messages[-1]["content"][0]["text"] = query
        completion = self._get_completion_base(
            messages=messages
        )
        return completion

    def get_completion_json_output(self, query: str) -> dict:
        """
        (for part 1)
        standard completion for a single query with no conversation history, with a json output
        :param query: user query
        :return: assistant response as a json object
        """
        messages = chat_prompt_template.copy()
        messages[0]["content"][0]["text"] = json_sys_prompt
        messages[-1]["content"][0]["text"] = query
        completion = self._get_completion_base(
            messages=messages,
            response_format={"type": "json_object"}
        )
        try:
            return json.loads(completion)
        except json.JSONDecodeError:
            return {"output_content": completion}

    def get_completion_json(self, message) -> dict:
        """
        (for part 2)
        standard jsonification of a message
        :param message:
        :return:
        """
        completion = self._get_completion_base(
            messages=message,
            response_format={"type": "json_object"}
        )
        try:
            return json.loads(completion)
        except json.JSONDecodeError:
            raise Exception("Error in parsing the output as JSON object")
            # return {"output_content": completion}

    def get_completion(self, message, history) -> str:
        """
        (for part 2)
        standard completion for a message with a conversation history
        :param message:
        :param history:
        :return:
        """
        completion = self._get_completion_base(
            messages=history + message
        )
        return completion