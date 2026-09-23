def test_simple():
    # 16 simple tests
    w = "weight"
    edges = [(0, 0, 1), (0, 0, 1.5), (0, 1, 2), (1, 0, 3)]
    for g1 in [nx.Graph(), nx.DiGraph(), nx.MultiGraph(), nx.MultiDiGraph()]:

        g1.add_weighted_edges_from(edges)
        g2 = g1.subgraph(g1.nodes())
        if g1.is_multigraph():
            em = iso.numerical_multiedge_match("weight", 1)
        else:
            em = iso.numerical_edge_match("weight", 1)
        assert nx.is_isomorphic(g1, g2, edge_match=em)

        for mod1, mod2 in [(False, True), (True, False), (True, True)]:
            # mod1 tests a regular edge
            # mod2 tests a selfloop
            if g2.is_multigraph():
                if mod1:
                    data1 = {0: {"weight": 10}}
                if mod2:
                    data2 = {0: {"weight": 1}, 1: {"weight": 2.5}}
            else:
                if mod1:
                    data1 = {"weight": 10}
                if mod2:
                    data2 = {"weight": 2.5}

            g2 = g1.subgraph(g1.nodes()).copy()
            if mod1:
                if not g1.is_directed():
                    g2._adj[1][0] = data1
                    g2._adj[0][1] = data1
                else:
                    g2._succ[1][0] = data1
                    g2._pred[0][1] = data1
            if mod2:
                if not g1.is_directed():
                    g2._adj[0][0] = data2
                else:
                    g2._succ[0][0] = data2
                    g2._pred[0][0] = data2

            assert not nx.is_isomorphic(g1, g2, edge_match=em)
