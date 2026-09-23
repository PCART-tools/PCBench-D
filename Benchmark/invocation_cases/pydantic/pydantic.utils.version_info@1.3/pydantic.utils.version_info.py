from pydantic.utils import version_info
import inspect

def main():
    result = version_info()
    print("version_info result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(version_info))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()