import networkx as nx
import inspect

def main():
    # Create two simple trees
    T1 = nx.path_graph(3)
    T2 = nx.path_graph(3)

    # Make rooted trees
    R1 = (T1, 0)
    R2 = (T2, 0)

    # Join the trees
    result = nx.join([R1, R2])
    print("join result nodes:", result.nodes())
    print("join result edges:", result.edges())

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(nx.join))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()