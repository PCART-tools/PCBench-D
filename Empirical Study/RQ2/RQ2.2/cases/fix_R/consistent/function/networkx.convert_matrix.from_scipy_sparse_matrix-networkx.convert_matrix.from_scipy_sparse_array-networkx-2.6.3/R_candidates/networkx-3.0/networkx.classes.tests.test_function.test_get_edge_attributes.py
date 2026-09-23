def test_get_edge_attributes():
    graphs = [nx.Graph(), nx.DiGraph(), nx.MultiGraph(), nx.MultiDiGraph()]
    for G in graphs:
        G = nx.path_graph(3, create_using=G)
        attr = "hello"
        vals = 100
        nx.set_edge_attributes(G, vals, attr)
        attrs = nx.get_edge_attributes(G, attr)

        assert len(attrs) == 2
        if G.is_multigraph():
            keys = [(0, 1, 0), (1, 2, 0)]
            for u, v, k in keys:
                try:
                    assert attrs[(u, v, k)] == 100
                except KeyError:
                    assert attrs[(v, u, k)] == 100
        else:
            keys = [(0, 1), (1, 2)]
            for u, v in keys:
                try:
                    assert attrs[(u, v)] == 100
                except KeyError:
                    assert attrs[(v, u)] == 100
