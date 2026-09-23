import networkx as nx
import inspect

def main():
    # Create a simple forest graph
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (4, 5)])
    
    # Use the forest_str function
    result = nx.forest_str(G)
    print("forest_str result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(nx.forest_str))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()