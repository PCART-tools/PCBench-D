import dask.bag as db
import inspect

def main():
    bag1 = db.from_sequence([1, 2, 3])
    concatenated_bag = db.Bag.concat(bag1)
    print("done")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(db.Bag.concat))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()