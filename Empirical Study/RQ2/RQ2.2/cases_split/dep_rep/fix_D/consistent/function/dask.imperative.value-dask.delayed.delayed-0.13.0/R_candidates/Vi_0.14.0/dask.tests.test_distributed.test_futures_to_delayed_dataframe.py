def test_futures_to_delayed_dataframe(loop):
    pd = pytest.importorskip('pandas')
    dd = pytest.importorskip('dask.dataframe')
    df = pd.DataFrame({'x': [1, 2, 3]})
    with cluster() as (s, [a, b]):
        with Client(s['address'], loop=loop) as c:  # flake8: noqa
            futures = c.scatter([df, df])
            ddf = dd.from_delayed(futures)
            dd.utils.assert_eq(ddf.compute(), pd.concat([df, df], axis=0))

            with pytest.raises(TypeError):
                ddf = dd.from_delayed([1, 2])
