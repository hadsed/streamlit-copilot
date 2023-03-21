import logging
import json
import os
from textwrap import dedent
from typing import List

import openai


openai.api_key = os.getenv("OPENAI_API_KEY")


logger = logging.getLogger(__name__)


class OpenAiCompletionModel:
    MODEL_TYPES = [
        "gpt-3.5-turbo",     # chat, 4k tokens
        "text-davinci-003",  # general completion, 4k tokens
        "code-davinci-002",  # code completion, 8k tokens
        "text-ada-001",      # fast completion, 2k tokens
    ]

    def __init__(self, name: str = "text-davinci-003"):
        self.name = name

    def run(self, prompt: str, **kwargs):
        response = openai.Completion.create(
            model=self.name, prompt=prompt, **kwargs)
        return response.choices[0].text


class OpenAiChatModel:

    def __init__(self, name: str = "gpt-3.5-turbo"):
        self.name = name

    def run(self, prompt: str, **kwargs):
        response = openai.ChatCompletion.create(
            model=self.name,
            messages=[
                {"role": "system", "content": "You are a code transformation assistant."},
                {"role": "user", "content": prompt},
            ]
        )
        return response.choices[0]['message']['content']


class CodeTransformer:
    """Takes a code file and a set of instructions and transforms the code,
    returning the new code file.
    """

    def __init__(self, name: str = "gpt-3.5-turbo"):
        self.name = name

    def run_model(self, prompt: str, **kwargs) -> str:
        response = openai.ChatCompletion.create(
            model=self.name,
            messages=[
                {"role": "system", "content": "You are a code transformation assistant."},
                {"role": "user", "content": prompt},
            ]
        )
        return response.choices[0]['message']['content']

    @staticmethod
    def build_prompt(code: str, instructions: str) -> str:
        prompt_lines = (
            [
                '```python',
            ] +
            code.split('\n') +
            [
                "```",
                "Instructions:",
            ] +
            instructions.split('\n') +
            ["", ""] +
            [
                ' '.join(dedent("""
                    Transform the code above to match the instructions and 
                    output the full code file. Valid python code only.
                    Any UI or visualizations will use Streamlit.
                    If you have comments, ensure they are valid Python comments.
                    Explain your interpretation as comments inlined with the code.
                """).split('\n'))
            ]
        )
        prompt = '\n'.join(prompt_lines)
        return prompt

    def extract_code_from_response(self, response):
        return response.split('```python')[-1].split('```')[0]

    def run(self, code: str, instructions: str, **kwargs) -> List[str]:
        prompt = self.build_prompt(code, instructions)
        response = self.run_model(prompt, **kwargs)
        return self.extract_code_from_response(response)


class CodeExtractor:
    """Takes a code file and a set of instructions and extracts the relevant
    code, returning a list of code snippets.
    """

    def __init__(self, name: str = "gpt-3.5-turbo"):
        self.name = name

    def run_model(self, prompt: str, **kwargs):
        response = openai.ChatCompletion.create(
            model=self.name,
            messages=[
                {"role": "system", "content": "You are a code extraction assistant."},
                {"role": "user", "content": prompt},
            ]
        )
        return response.choices[0]['message']['content']

    @staticmethod
    def build_prompt(code: str, instructions: str) -> str:
        prompt_lines = (
            [
                '```python',
            ] +
            code.split('\n') +
            [
                "```",
                "Instructions:",
            ] +
            instructions.split('\n') +
            ["", ""] +
            [
                ' '.join(dedent("""
                    Extract snippets of the code above according to the instructions.
                    Format as a JSON list of strings. Do not modify the code in any way.
                    Valid python code only. If you have comments, ensure they are
                    valid Python comments. Explain your interpretation as comments.
                """).split('\n'))
            ]
        )
        prompt = '\n'.join(prompt_lines)
        return prompt

    def parse_response(self, response: str) -> List[str]:
        code_snippets = json.loads(response)
        return code_snippets

    def run(self, code: str, instructions: str, **kwargs) -> List[str]:
        prompt = self.build_prompt(code, instructions)
        response = self.run_model(prompt, **kwargs)
        logger.debug(f"Response:\n\n{response}")
        code_snippets = self.parse_response(response)
        return code_snippets
