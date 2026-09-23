def test_named_value():
    assert 'X' in delayed(1, name='X').dask
