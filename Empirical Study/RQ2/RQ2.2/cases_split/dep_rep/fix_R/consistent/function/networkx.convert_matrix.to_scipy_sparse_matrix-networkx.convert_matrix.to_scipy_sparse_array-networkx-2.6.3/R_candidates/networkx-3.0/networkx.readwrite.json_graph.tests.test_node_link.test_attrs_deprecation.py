def test_attrs_deprecation(recwarn):
    G = nx.path_graph(3)

    # No warnings when `attrs` kwarg not used
    data = node_link_data(G)
    H = node_link_graph(data)
    assert len(recwarn) == 0

    # Future warning raised with `attrs` kwarg
    attrs = dict(source="source", target="target", name="id", key="key", link="links")
    data = node_link_data(G, attrs=attrs)
    assert len(recwarn) == 1

    recwarn.clear()
    H = node_link_graph(data, attrs=attrs)
    assert len(recwarn) == 1
