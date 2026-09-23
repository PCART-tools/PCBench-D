def test_null_graph():
    G = nx.Graph()
    _check_augmentations(G, max_k=MAX_EFFICIENT_K + 2)
