def test_map_partitions_names():
    npartitions = 3
    ddf = dd.from_pandas(df, npartitions)

    res = ddf.map_overlap(shifted_sum, 0, 3, 0, 3, c=2)
    res2 = ddf.map_overlap(shifted_sum, 0, 3, 0, 3, c=2)
    assert set(res.dask) == set(res2.dask)

    res3 = ddf.map_overlap(shifted_sum, 0, 3, 0, 3, c=3)
    assert res3._name != res._name
    # Difference is just the final map
    diff = set(res3.dask).difference(res.dask)
    assert len(diff) == npartitions

    res4 = ddf.map_overlap(shifted_sum, 3, 0, 0, 3, c=2)
    assert res4._name != res._name
