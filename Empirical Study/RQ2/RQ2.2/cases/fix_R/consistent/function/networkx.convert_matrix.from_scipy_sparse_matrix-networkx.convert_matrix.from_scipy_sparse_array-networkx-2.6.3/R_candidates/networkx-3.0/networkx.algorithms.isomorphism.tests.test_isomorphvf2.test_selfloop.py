def test_selfloop():
    # Simple test for graphs with selfloops
    edges = [
        (0, 1),
        (0, 2),
        (1, 2),
        (1, 3),
        (2, 2),
        (2, 4),
        (3, 1),
        (3, 2),
        (4, 2),
        (4, 5),
        (5, 4),
    ]
    nodes = list(range(6))

    for g1 in [nx.Graph(), nx.DiGraph()]:
        g1.add_edges_from(edges)
        for _ in range(100):
            new_nodes = list(nodes)
            random.shuffle(new_nodes)
            d = dict(zip(nodes, new_nodes))
            g2 = nx.relabel_nodes(g1, d)
            if not g1.is_directed():
                gm = iso.GraphMatcher(g1, g2)
            else:
                gm = iso.DiGraphMatcher(g1, g2)
            assert gm.is_isomorphic()
