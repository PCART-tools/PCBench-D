import networkx as nx
from networkx.algorithms.approximation import maximum_independent_set
import inspect

def main():
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)])
    result = maximum_independent_set(G)
    print("maximum_independent_set result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(maximum_independent_set))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()