@pytest.mark.skipif(no_backends_for_leiden_communities)
def test_directed_not_implemented():
    G = nx.cycle_graph(4, create_using=nx.DiGraph)
    with pytest.raises(nx.NetworkXNotImplemented):
        nx.community.leiden_communities(G)
