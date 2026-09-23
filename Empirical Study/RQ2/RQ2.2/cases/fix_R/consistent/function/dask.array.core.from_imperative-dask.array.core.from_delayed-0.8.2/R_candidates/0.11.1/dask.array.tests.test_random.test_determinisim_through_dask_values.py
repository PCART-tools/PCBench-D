def test_determinisim_through_dask_values():
    samples_1 = da.random.RandomState(42).normal(size=1000, chunks=10)
    samples_2 = da.random.RandomState(42).normal(size=1000, chunks=10)

    assert [v for k, v in sorted(samples_1.dask.items())] ==\
           [v for k, v in sorted(samples_2.dask.items())]
