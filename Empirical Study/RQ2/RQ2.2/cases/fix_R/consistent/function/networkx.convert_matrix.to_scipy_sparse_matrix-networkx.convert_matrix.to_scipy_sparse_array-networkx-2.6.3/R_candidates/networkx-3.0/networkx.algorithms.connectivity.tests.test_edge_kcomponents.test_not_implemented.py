def test_not_implemented():
    G = nx.MultiGraph()
    pytest.raises(nx.NetworkXNotImplemented, EdgeComponentAuxGraph.construct, G)
    pytest.raises(nx.NetworkXNotImplemented, nx.k_edge_components, G, k=2)
    pytest.raises(nx.NetworkXNotImplemented, nx.k_edge_subgraphs, G, k=2)
    with pytest.raises(nx.NetworkXNotImplemented):
        next(bridge_components(G))
    with pytest.raises(nx.NetworkXNotImplemented):
        next(bridge_components(nx.DiGraph()))
