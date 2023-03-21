import logging

from streamlit_copilot.copilot.model import CodeTransformer


logger = logging.getLogger(__name__)


class Copilot:

    def __init__(self, app_path: str):
        self.app_path = app_path
        self.command_count = 0
        self.command_log = []
        self.code_transformer = CodeTransformer()

    def command(self, user_input):
        self.command_log.append(user_input)
        self.command_count += 1
        self.act(user_input)
        return self.response()

    def get_current_code(self):
        with open(self.app_path, 'r') as f:
            return f.read()

    def write_new_code(self, new_code):
        with open(self.app_path, 'w') as f:
            f.writelines(new_code)

    def act(self, instructions):
        code = self.get_current_code()
        logger.debug(f"Executing model...")
        new_code = self.code_transformer.run(code, instructions)
        logger.debug(f"Model executed.")
        self.write_new_code(new_code)

    def response(self):
        return f'''Modified code.'''
