from rich.console import Console
from rich.bar import Bar
import inspect

def main():
    console = Console()

    bar = Bar(
        100,
        60,
        40,
    )

    console.print("Rendering Bar:")
    console.print(bar)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Bar))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()