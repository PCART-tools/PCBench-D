def test_barbell():
    G = nx.barbell_graph(5, 0)
    _check_augmentations(G)

    G = nx.barbell_graph(5, 2)
    _check_augmentations(G)

    G = nx.barbell_graph(5, 3)
    _check_augmentations(G)

    G = nx.barbell_graph(5, 4)
    _check_augmentations(G)
