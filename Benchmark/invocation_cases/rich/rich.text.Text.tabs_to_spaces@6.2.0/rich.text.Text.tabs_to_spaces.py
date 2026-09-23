from rich.text import Text
import inspect

def main():
    text = Text("Hello\tWorld")
    result = text.tabs_to_spaces()
    print("tabs_to_spaces result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Text.tabs_to_spaces))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()