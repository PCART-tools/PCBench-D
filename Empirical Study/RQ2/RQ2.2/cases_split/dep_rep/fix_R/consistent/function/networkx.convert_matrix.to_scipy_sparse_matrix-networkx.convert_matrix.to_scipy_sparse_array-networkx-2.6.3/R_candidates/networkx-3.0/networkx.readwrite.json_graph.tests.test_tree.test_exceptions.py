def test_exceptions():
    with pytest.raises(TypeError, match="is not a tree."):
        G = nx.complete_graph(3)
        tree_data(G, 0)
    with pytest.raises(TypeError, match="is not directed."):
        G = nx.path_graph(3)
        tree_data(G, 0)
    with pytest.raises(TypeError, match="is not weakly connected."):
        G = nx.path_graph(3, create_using=nx.DiGraph)
        G.add_edge(2, 0)
        G.add_node(3)
        tree_data(G, 0)
    with pytest.raises(nx.NetworkXError, match="must be different."):
        G = nx.MultiDiGraph()
        G.add_node(0)
        tree_data(G, 0, ident="node", children="node")
