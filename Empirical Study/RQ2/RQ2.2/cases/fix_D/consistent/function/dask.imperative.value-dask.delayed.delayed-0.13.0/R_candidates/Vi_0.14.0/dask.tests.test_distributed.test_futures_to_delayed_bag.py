def test_futures_to_delayed_bag(loop):
    db = pytest.importorskip('dask.bag')
    L = [1, 2, 3]
    with cluster() as (s, [a, b]):
        with Client(s['address'], loop=loop) as c:  # flake8: noqa
            futures = c.scatter([L, L])
            b = db.from_delayed(futures)
            assert list(b) == L + L
