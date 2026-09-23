import spacy
import inspect

def main():
    package_name = "en_core_web_sm"
    result = spacy.util.get_package(package_name)
    print("get_package result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(spacy.util.get_package))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()