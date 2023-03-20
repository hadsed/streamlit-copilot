import os
import subprocess
import click
from textwrap import dedent, indent

from streamlit_copilot.copilot import Copilot


APP_PATH = 'app/app.py'
HELP_TEXT = dedent("""
    /go     Execute the commands you've entered
    /exit   Exit the app
    /help   Show this help text
""")



def run_app():
    port = '8501'
    app_url = f'http://localhost:{port}'
    env = os.environ.copy()
    env.update({
        'STREAMLIT_SERVER_PORT': port,
        'STREAMLIT_SERVER_RUN_ON_SAVE': 'true',
    })
    process = subprocess.Popen(
        ['streamlit', 'run', APP_PATH],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )
    return process, app_url


@click.command()
def cli():
    process, app_url = run_app()
    click.echo(indent(dedent(f"""


        ..:::   Welcome to streamlit-copilot.   :::..

        
        {indent(HELP_TEXT, ' '*8)}


        Your app is running on {app_url}
        
    """), ' '*4))
    copilot = Copilot(app_path=APP_PATH)
    command_count = 0
    while True:
        print_command_input_header(command_count)
        user_input = input()
        command_buffer = []
        if user_input == '/exit':
            process.kill()
            break
        elif user_input == '/go':
            copilot.instruct(command_buffer)
            print_copilot_response_header(command_count)
            print_copilot_response(copilot.response())
            print_separator()
            command_buffer = []
            command_count += 1
        else:
            command_buffer.append(user_input)


def print_command_input_header(command_count):
    click.echo(dedent(f"""
        +-------------------+
        | [{command_count}]  Command:     |
        +-------------------+
    """))


def print_copilot_response_header(command_count):
    click.echo(dedent(f"""
        +----------------------------+
        | [{command_count}]  Copilot Response:     |
        +----------------------------+
    """))


def print_copilot_response(response):
    click.echo(dedent(f"""
        {response}
    """))


def print_separator():
    sep = '='*35
    click.echo(dedent(f"""
        {sep}
    """))
