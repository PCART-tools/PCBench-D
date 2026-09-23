def test_exception():
    with pytest.raises(nx.NetworkXError):
        G = nx.MultiDiGraph()
        cytoscape_data(G, name="foo", ident="foo")
