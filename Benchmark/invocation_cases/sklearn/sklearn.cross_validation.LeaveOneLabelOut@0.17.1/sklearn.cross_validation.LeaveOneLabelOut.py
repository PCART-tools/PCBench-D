import numpy as np
from sklearn.cross_validation import LeaveOneLabelOut
import inspect

def main():
    labels = np.array([1, 1, 2, 2, 3, 3])
    loo = LeaveOneLabelOut(labels)
    for train_index, test_index in loo:
        print("TRAIN:", train_index, "TEST:", test_index)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(LeaveOneLabelOut))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()