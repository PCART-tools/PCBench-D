import networkx as nx
import inspect

def main():
    G = nx.OrderedGraph()
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    result = list(G.edges)
    print("OrderedGraph edges:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(nx.OrderedGraph))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()