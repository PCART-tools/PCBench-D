import inspect
from spacy.util import get_package_by_name



def main():
    # Simulate a model load
    model = get_package_by_name("en",'.')
    print("Loaded model:", model)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(get_package_by_name))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
