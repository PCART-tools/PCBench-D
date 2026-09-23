def test_index_with_int_dask_array_nocompute():
    """ Test that when the indices are a dask array
    they are not accidentally computed
    """
    def crash():
        raise NotImplementedError()

    x = da.arange(5, chunks=-1)
    idx = da.Array({('x', 0): (crash,)}, name='x',
                   chunks=((2,), ), dtype=np.int64)
    result = x[idx]
    with pytest.raises(NotImplementedError):
        result.compute()
