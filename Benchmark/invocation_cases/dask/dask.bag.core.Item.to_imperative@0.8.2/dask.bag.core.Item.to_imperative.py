import dask.bag as db
import inspect

def main():
    data = [1, 2, 3, 4, 5]
    bag = db.from_sequence(data)
    item = bag.sum()
    imperative_result = item.to_imperative()
    print("to_imperative result:", imperative_result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(db.Item.to_imperative))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()