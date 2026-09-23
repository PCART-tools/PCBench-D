import networkx as nx
import inspect

def main():
    G = nx.DiGraph()
    G.add_weighted_edges_from([(0, 1, 5), (1, 2, 3), (0, 2, 10)])
    length, path = nx.bellman_ford(G, source=0)
    print("Bellman-Ford result:", length, path)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(nx.bellman_ford))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()