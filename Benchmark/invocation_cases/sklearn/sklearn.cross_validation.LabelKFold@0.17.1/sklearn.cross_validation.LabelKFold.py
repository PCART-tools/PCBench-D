import numpy as np
from sklearn.cross_validation import LabelKFold
import inspect

def main():
    labels = np.array([0, 0, 1, 1, 2, 2])
    lkf = LabelKFold(labels, n_folds=3)
    result = list(lkf)
    print("LabelKFold result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(LabelKFold))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()