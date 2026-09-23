import networkx as nx
from networkx.algorithms.community.quality import coverage
import inspect

def main():
    G = nx.karate_club_graph()
    communities = [{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}, set(G.nodes) - {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}]
    result = coverage(G, communities)
    print("Coverage result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(coverage))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()