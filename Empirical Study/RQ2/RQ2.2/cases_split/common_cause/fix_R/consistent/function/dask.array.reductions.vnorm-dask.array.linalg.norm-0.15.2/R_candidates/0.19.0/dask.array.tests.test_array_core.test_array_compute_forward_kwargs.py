def test_array_compute_forward_kwargs():
    x = da.arange(10, chunks=2).sum()
    x.compute(bogus_keyword=10)
