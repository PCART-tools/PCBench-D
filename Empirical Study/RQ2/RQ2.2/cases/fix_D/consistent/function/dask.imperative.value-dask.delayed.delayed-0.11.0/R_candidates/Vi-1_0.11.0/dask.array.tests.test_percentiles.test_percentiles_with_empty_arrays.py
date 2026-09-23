def test_percentiles_with_empty_arrays():
    x = da.ones(10, chunks=((5, 0, 5),))
    assert da.percentile(x, [10, 50, 90]).compute().tolist() == [1, 1, 1]
