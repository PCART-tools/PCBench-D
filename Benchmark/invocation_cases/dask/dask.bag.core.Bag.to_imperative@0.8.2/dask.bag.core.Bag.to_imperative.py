import dask.bag as db
import inspect

def main():
    # Create a Dask bag with sample data
    data = [1, 2, 3, 4, 5]
    bag = db.from_sequence(data)

    # Call the target API
    result = bag.to_imperative()
    print("to_imperative result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(db.Bag.to_imperative))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()