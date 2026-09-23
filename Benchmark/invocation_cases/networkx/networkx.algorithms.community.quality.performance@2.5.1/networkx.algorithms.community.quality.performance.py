import networkx as nx
from networkx.algorithms.community.quality import performance
import inspect

def main():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])
    communities = [{0, 1}, {2, 3}]
    result = performance(G, communities)
    print("performance result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(performance))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()