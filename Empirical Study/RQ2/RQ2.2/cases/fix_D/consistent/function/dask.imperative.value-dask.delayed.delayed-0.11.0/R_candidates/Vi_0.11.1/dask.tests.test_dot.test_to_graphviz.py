def test_to_graphviz():
    g = to_graphviz(dsk)
    labels = list(filter(None, map(get_label, g.body)))
    assert len(labels) == 10        # 10 nodes total
    funcs = set(('add', 'sum', 'neg'))
    assert set(labels).difference(dsk) == funcs
    assert set(labels).difference(funcs) == set(dsk)
