import networkx as nx
import inspect

def main():
    G = nx.karate_club_graph()
    communities = nx.algorithms.community.modularity_max._naive_greedy_modularity_communities(G)
    print("Communities:", list(communities))

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(nx.algorithms.community.modularity_max._naive_greedy_modularity_communities))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()