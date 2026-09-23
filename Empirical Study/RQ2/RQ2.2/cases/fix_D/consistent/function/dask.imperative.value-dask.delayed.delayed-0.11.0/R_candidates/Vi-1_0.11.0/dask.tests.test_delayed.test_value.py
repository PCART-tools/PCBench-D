def test_value():
    v = delayed(1)
    assert v.compute() == 1
    assert 1 in v.dask.values()
