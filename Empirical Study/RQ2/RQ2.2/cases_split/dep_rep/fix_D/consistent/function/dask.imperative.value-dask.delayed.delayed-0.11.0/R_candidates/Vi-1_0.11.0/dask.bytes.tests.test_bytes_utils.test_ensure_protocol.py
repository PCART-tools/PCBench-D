def test_ensure_protocol():
    try:
        import hdfs3  # noqa: F401
        pytest.skip()
    except ImportError:
        pass

    dd = pytest.importorskip('dask.dataframe')
    try:
        dd.read_csv('hdfs://data/*.csv')
    except RuntimeError as e:
        assert "hdfs3" in str(e)
