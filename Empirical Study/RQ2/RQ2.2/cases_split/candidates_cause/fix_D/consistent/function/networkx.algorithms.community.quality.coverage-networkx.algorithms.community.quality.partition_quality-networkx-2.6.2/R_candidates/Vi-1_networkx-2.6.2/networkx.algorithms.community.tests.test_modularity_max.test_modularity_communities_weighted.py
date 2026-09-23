def test_modularity_communities_weighted():
    G = nx.balanced_tree(2, 3)
    for (a, b) in G.edges:
        if ((a == 1) or (a == 2)) and (b != 0):
            G[a][b]["weight"] = 10.0
        else:
            G[a][b]["weight"] = 1.0

    expected = [{0, 1, 3, 4, 7, 8, 9, 10}, {2, 5, 6, 11, 12, 13, 14}]

    assert greedy_modularity_communities(G, weight="weight") == expected
