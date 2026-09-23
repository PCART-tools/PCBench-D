@pytest.mark.parametrize('chunks', [2, 4])
def test_index_with_int_dask_array_indexerror(chunks):
    a = da.arange(4, chunks=chunks)
    idx = da.from_array([4], chunks=1)
    with pytest.raises(IndexError):
        a[idx].compute()
    idx = da.from_array([-5], chunks=1)
    with pytest.raises(IndexError):
        a[idx].compute()
