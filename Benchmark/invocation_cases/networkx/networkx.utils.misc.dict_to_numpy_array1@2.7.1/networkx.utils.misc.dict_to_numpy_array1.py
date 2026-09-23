import networkx as nx
import inspect
import numpy as np

def main():
    d = {'a': 1, 'b': 2, 'c': 3}
    result = nx.utils.dict_to_numpy_array1(d)
    print("dict_to_numpy_array1 result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(nx.utils.dict_to_numpy_array1))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()