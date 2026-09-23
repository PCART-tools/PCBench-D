import numpy as np
from sklearn.metrics import jaccard_similarity_score
import inspect

def main():
    y_true = np.array([0, 1, 1, 1])
    y_pred = np.array([1, 1, 0, 1])
    result = jaccard_similarity_score(y_true, y_pred)
    print("jaccard_similarity_score result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(jaccard_similarity_score))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()