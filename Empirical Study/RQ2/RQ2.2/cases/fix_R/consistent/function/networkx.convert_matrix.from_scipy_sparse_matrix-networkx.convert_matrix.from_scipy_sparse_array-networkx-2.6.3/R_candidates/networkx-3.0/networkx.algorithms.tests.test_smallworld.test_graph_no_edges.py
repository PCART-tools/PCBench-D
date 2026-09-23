@pytest.mark.parametrize("f", (nx.random_reference, nx.lattice_reference))
def test_graph_no_edges(f):
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3])
    with pytest.raises(nx.NetworkXError, match="Graph has fewer that 2 edges"):
        f(G)
