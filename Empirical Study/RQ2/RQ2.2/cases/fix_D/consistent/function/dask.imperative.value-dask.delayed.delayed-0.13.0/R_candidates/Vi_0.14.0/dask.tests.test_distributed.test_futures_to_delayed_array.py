def test_futures_to_delayed_array(loop):
    da = pytest.importorskip('dask.array')
    from dask.array.utils import assert_eq
    np = pytest.importorskip('numpy')
    x = np.arange(5)
    with cluster() as (s, [a, b]):
        with Client(s['address'], loop=loop) as c:  # flake8: noqa
            futures = c.scatter([x, x])
            A = da.concatenate([da.from_delayed(f, shape=x.shape, dtype=x.dtype)
                                for f in futures], axis=0)
            assert_eq(A.compute(), np.concatenate([x, x], axis=0))
