def test_castra_column_store():
    castra = pytest.importorskip('castra')
    blosc = pytest.importorskip('blosc')
    if (LooseVersion(blosc.__version__) == '1.3.0' or
            LooseVersion(castra.__version__) < '0.1.8'):
        pytest.skip()

    df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})

    with castra.Castra(template=df) as c:
        c.extend(df)

        df = c.to_dask()

        df2 = df[['x']]

        dsk = dd.optimize(df2.dask, df2._keys())

        assert dsk == {(df2._name, 0): (castra.Castra.load_partition, c, '0--2',
                                            (list, ['x']))}
        df3 = df.index
        dsk = dd.optimize(df3.dask, df3._keys())
        assert dsk == {(df3._name, 0): (castra.Castra.load_index, c, '0--2')}
