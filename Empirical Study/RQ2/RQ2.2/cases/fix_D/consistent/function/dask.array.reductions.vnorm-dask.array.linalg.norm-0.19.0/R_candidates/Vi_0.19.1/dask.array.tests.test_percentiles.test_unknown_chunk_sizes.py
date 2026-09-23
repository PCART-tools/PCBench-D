def test_unknown_chunk_sizes():
    x = da.random.random(1000, chunks=(100,))
    x._chunks = ((np.nan,) * 10,)

    result = da.percentile(x, 50).compute()
    assert 0.1 < result < 0.9

    a, b = da.percentile(x, [40, 60]).compute()
    assert 0.1 < a < 0.9
    assert 0.1 < b < 0.9
    assert a < b
