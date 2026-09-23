import networkx as nx
import inspect

def main():
    # Example usage of _dispatch
    def example_function(x):
        return x * 2

    dispatched_function = nx.utils.backends._dispatch(example_function)
    result = dispatched_function(5)
    print("Dispatched function result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(nx.utils.backends._dispatch))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()