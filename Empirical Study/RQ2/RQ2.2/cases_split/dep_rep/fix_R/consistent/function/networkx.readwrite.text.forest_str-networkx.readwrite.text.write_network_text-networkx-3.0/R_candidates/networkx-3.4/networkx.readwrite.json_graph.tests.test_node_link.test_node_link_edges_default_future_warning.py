def test_node_link_edges_default_future_warning():
    "Test FutureWarning is raised when `edges=None` in node_link_data and node_link_graph"
    G = nx.Graph([(1, 2)])
    with pytest.warns(FutureWarning, match="\nThe default value will be"):
        data = nx.node_link_data(G)  # edges=None, the default
    with pytest.warns(FutureWarning, match="\nThe default value will be"):
        H = nx.node_link_graph(data)  # edges=None, the default
