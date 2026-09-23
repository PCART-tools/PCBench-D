import dask.array as da
import inspect
import numpy as np

def main():
    # Create a Dask array
    x = da.from_array(np.array([[3, 4], [6, 8]]), chunks=(2, 2))
    
    # Call the vnorm function
    result = da.reductions.vnorm(x, ord=2)
    print("vnorm result:", result.compute())

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(da.reductions.vnorm))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()