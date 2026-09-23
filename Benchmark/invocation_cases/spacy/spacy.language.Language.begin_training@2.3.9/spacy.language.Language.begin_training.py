import spacy
from spacy.language import Language
import inspect

def main():
    nlp = spacy.blank("en")
    result = Language.begin_training(nlp)
    print("begin_training result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Language.begin_training))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()