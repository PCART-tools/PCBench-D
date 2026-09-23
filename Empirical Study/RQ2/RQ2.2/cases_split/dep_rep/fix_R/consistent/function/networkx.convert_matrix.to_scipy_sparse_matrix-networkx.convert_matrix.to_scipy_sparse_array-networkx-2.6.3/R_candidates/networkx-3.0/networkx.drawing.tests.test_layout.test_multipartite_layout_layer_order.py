def test_multipartite_layout_layer_order():
    """Return the layers in sorted order if the layers of the multipartite
    graph are sortable. See gh-5691"""
    G = nx.Graph()
    for node, layer in zip(("a", "b", "c", "d", "e"), (2, 3, 1, 2, 4)):
        G.add_node(node, subset=layer)

    # Horizontal alignment, therefore y-coord determines layers
    pos = nx.multipartite_layout(G, align="horizontal")

    # Nodes "a" and "d" are in the same layer
    assert pos["a"][-1] == pos["d"][-1]
    # positions should be sorted according to layer
    assert pos["c"][-1] < pos["a"][-1] < pos["b"][-1] < pos["e"][-1]

    # Make sure that multipartite_layout still works when layers are not sortable
    G.nodes["a"]["subset"] = "layer_0"  # Can't sort mixed strs/ints
    pos_nosort = nx.multipartite_layout(G)  # smoke test: this should not raise
    assert pos_nosort.keys() == pos.keys()
