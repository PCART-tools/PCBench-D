def test_aliases():
    g = to_graphviz({'x': 1, 'y': 'x'})
    labels = list(filter(None, map(get_label, g.body)))
    assert len(labels) == 2
    assert len(g.body) - len(labels) == 1   # Single edge
