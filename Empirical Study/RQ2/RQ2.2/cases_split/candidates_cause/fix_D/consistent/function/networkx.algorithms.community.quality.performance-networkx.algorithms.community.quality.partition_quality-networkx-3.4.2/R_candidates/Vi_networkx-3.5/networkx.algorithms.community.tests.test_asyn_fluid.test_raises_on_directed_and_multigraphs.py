@pytest.mark.parametrize("graph_constructor", (nx.DiGraph, nx.MultiGraph))
def test_raises_on_directed_and_multigraphs(graph_constructor):
    G = graph_constructor([(0, 1), (1, 2)])
    with pytest.raises(nx.NetworkXNotImplemented):
        nx.community.asyn_fluidc(G, 1)
