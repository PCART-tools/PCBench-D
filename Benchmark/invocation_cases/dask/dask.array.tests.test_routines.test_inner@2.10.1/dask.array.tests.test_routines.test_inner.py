import dask.array as da
from dask.array.tests.test_routines import test_inner as dask_test_inner
import inspect

def main():
    params = [((20,), (6,)), ((4, 5), (2, 3))]
    for shape1, shape2 in params:
        dask_test_inner(shape1, shape2)
        print("test_inner", shape1, shape2, "passed")
    
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(dask_test_inner))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()