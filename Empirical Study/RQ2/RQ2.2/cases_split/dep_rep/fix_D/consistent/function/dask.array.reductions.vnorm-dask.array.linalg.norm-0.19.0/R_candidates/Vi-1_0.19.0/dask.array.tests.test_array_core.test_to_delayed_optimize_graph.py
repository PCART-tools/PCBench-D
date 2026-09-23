def test_to_delayed_optimize_graph():
    x = da.ones((4, 4), chunks=(2, 2))
    y = x[1:][1:][1:][:, 1:][:, 1:][:, 1:]

    # optimizations
    d = y.to_delayed().flatten().tolist()[0]
    assert len([k for k in d.dask if k[0].startswith('getitem')]) == 1

    # no optimizations
    d2 = y.to_delayed(optimize_graph=False).flatten().tolist()[0]
    assert dict(d2.dask) == dict(y.dask)

    assert (d.compute() == d2.compute()).all()
