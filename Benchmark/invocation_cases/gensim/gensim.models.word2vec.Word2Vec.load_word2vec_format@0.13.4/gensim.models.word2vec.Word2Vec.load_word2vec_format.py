import inspect
import tempfile
from gensim.models import Word2Vec

def main():
    # Create a minimal Word2Vec text-format model file
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        f.write("2 2\n")
        f.write("hello 0.1 0.2\n")
        f.write("world 0.0 0.3\n")
        model_path = f.name

    # Load the model using the gensim 0.13.4 user-level API
    model = Word2Vec.load_word2vec_format(model_path, binary=False)
    print("Model loaded:", isinstance(model, Word2Vec))

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Word2Vec.load_word2vec_format))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
