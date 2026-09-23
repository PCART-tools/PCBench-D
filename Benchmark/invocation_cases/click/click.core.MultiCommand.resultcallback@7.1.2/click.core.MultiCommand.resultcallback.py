import click
import inspect
from click.testing import CliRunner

class MyCommands(click.MultiCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._commands = {}

    def list_commands(self, ctx):
        return sorted(self._commands.keys())

    def get_command(self, ctx, name):
        return self._commands.get(name)

    def command(self, name=None, **kwargs):
        def decorator(f):
            cmd = click.command(name=name, **kwargs)(f)
            self._commands[cmd.name] = cmd
            return cmd
        return decorator


@click.command(cls=MyCommands, chain=True)
def cli():
    pass

@cli.command()
@click.argument('name')
def greet(name):
    click.echo(f"Hello, {name}!")

@cli.resultcallback()
def process_result(result, **kwargs):
    click.echo("Processing result...")

def main():
    runner = CliRunner()
    result = runner.invoke(cli, ['greet', 'World'])
    print("Command result:", result.output.strip())
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(click.core.MultiCommand.resultcallback))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
