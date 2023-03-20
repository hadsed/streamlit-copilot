
class Copilot:

    def __init__(self, app_path: str):
        self.app_path = app_path
        self.command_count = 0
        self.command_log = []
    
    def instruct(self, user_input):
        self.act()

    def act(self):
        with open(self.app_path, 'r') as f:
            lines = f.readlines()
        with open(self.app_path, 'w') as f:
            code_line = ['\n', 'st.write("Hello World!")']
            lines.extend(code_line)
            f.writelines(lines)

    def response(self):
        return "My (the Copilot's) response to your command."
