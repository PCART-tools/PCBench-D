import numpy as np
from sklearn.cross_validation import LeavePLabelOut
import inspect

def main():
    labels = [1, 1, 2, 2, 3, 3]
    lp = LeavePLabelOut(labels, p=1)
    result = list(lp)
    print("LeavePLabelOut result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(LeavePLabelOut))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()