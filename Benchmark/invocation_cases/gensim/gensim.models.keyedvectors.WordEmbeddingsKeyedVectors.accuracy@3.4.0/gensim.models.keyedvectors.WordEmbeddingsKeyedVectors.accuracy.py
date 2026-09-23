import inspect
from gensim.test.utils import common_texts
from gensim.models import Word2Vec
from gensim.models.keyedvectors import WordEmbeddingsKeyedVectors

def main():
    model = Word2Vec(
        sentences=common_texts,
        window=5,
        min_count=1,
        workers=1
    )

    kv = model.wv 

    questions = "questions-words.txt"
    with open(questions, "w") as f:
        f.write(": capital-common-countries\n")
        f.write("Athens Greece Oslo Norway\n")

    result = WordEmbeddingsKeyedVectors.accuracy(kv, questions)

    print("accuracy result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(WordEmbeddingsKeyedVectors.accuracy))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()