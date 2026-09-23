import inspect
from sklearn.cross_validation import LabelShuffleSplit

def main():
    labels = [0, 1, 0, 1, 0, 1]
    lss = LabelShuffleSplit(labels, n_iter=3, test_size=0.5, random_state=42)
    for train_index, test_index in lss:
        print("TRAIN:", train_index, "TEST:", test_index)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(LabelShuffleSplit))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()