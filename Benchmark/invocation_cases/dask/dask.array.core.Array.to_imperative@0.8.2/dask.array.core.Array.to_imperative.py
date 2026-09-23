import dask.array as da
import inspect

def main():
    # Create a Dask array
    x = da.ones((3, 3), chunks=(2, 2))
    
    # Call the target API
    result = x.to_imperative()
    print("compute result:", result)
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(x.to_imperative))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()