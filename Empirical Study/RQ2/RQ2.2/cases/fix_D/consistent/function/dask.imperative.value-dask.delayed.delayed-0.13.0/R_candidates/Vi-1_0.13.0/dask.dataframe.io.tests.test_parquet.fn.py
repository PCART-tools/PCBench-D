@pytest.fixture
def fn(tmpdir):
    ddf = dd.from_pandas(df, npartitions=3)
    to_parquet(str(tmpdir), ddf)

    return str(tmpdir)
