def test_get_node_attributes():
    graphs = [nx.Graph(), nx.DiGraph(), nx.MultiGraph(), nx.MultiDiGraph()]
    for G in graphs:
        G = nx.path_graph(3, create_using=G)
        attr = "hello"
        vals = 100
        nx.set_node_attributes(G, vals, attr)
        attrs = nx.get_node_attributes(G, attr)
        assert attrs[0] == vals
        assert attrs[1] == vals
        assert attrs[2] == vals
