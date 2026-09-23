def test_n_communities_parameter():
    G = nx.circular_ladder_graph(4)

    # No aggregation:
    expected = [{k} for k in range(8)]
    assert greedy_modularity_communities(G, n_communities=8) == expected

    # Aggregation to half order (number of nodes)
    expected = [{k, k + 1} for k in range(0, 8, 2)]
    assert greedy_modularity_communities(G, n_communities=4) == expected

    # Default aggregation case (here, 2 communities emerge)
    expected = [frozenset(range(0, 4)), frozenset(range(4, 8))]
    assert greedy_modularity_communities(G, n_communities=1) == expected
