def test_determinisim_through_dask_values():
    samples_1 = da.random.RandomState(42).normal(size=1000, chunks=10)
    samples_2 = da.random.RandomState(42).normal(size=1000, chunks=10)

    assert set(samples_1.dask) == set(samples_2.dask)
    assert_eq(samples_1, samples_2)
