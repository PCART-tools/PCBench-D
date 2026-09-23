def test_star():
    G = nx.star_graph(3)
    _check_augmentations(G)

    G = nx.star_graph(5)
    _check_augmentations(G)

    G = nx.star_graph(10)
    _check_augmentations(G)
