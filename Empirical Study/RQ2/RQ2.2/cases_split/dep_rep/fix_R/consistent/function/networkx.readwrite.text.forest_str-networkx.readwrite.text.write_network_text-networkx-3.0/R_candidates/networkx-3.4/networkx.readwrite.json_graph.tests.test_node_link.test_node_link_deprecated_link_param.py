def test_node_link_deprecated_link_param():
    G = nx.Graph([(1, 2)])
    with pytest.warns(DeprecationWarning, match="Keyword argument 'link'"):
        data = nx.node_link_data(G, link="links")
    with pytest.warns(DeprecationWarning, match="Keyword argument 'link'"):
        H = nx.node_link_graph(data, link="links")
