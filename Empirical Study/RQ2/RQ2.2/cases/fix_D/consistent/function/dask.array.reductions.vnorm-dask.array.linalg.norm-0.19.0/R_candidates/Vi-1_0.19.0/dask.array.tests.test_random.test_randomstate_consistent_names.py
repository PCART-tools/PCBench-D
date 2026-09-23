def test_randomstate_consistent_names():
    state1 = da.random.RandomState(42)
    state2 = da.random.RandomState(42)
    assert (sorted(state1.normal(size=(100, 100), chunks=(10, 10)).dask) ==
            sorted(state2.normal(size=(100, 100), chunks=(10, 10)).dask))
    assert (sorted(state1.normal(size=100, loc=4.5, scale=5.0, chunks=10).dask) ==
            sorted(state2.normal(size=100, loc=4.5, scale=5.0, chunks=10).dask))
