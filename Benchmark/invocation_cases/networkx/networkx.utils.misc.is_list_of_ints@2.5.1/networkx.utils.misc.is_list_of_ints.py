import networkx as nx
from networkx.utils.misc import is_list_of_ints
import inspect

def main():
    test_data = [1, 2, 3, 4]
    result = is_list_of_ints(test_data)
    print("is_list_of_ints result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(is_list_of_ints))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()