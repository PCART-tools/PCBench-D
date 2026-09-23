import click
import inspect

@click.group()
@click.pass_context
def cli(ctx):
    pass

@cli.resultcallback()
def process_result(result, **kwargs):
    print("Result callback invoked with:", result)

@cli.command()
def hello():
    return "Hello, World!"

def main():
    cli(["hello"], standalone_mode=False)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(click.Group.resultcallback))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()