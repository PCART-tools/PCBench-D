def test_optimize_graph_false():
    from dask.callbacks import Callback
    d = {'x': 1, 'y': (inc, 'x'), 'z': (add, 10, 'y')}
    keys = []
    with Callback(pretask=lambda key, *args: keys.append(key)):
        get(d, 'z', optimize_graph=False)
    assert len(keys) == 2
