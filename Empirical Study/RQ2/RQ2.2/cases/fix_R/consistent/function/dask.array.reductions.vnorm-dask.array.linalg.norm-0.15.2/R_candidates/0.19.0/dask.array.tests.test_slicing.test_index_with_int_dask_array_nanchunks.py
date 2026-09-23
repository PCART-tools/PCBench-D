@pytest.mark.parametrize('chunks', [1, 2, 3, 4, 5])
def test_index_with_int_dask_array_nanchunks(chunks):
    # Slice by array with nan-sized chunks
    a = da.arange(-2, 3, chunks=chunks)
    assert_eq(a[a.nonzero()], np.array([-2, -1,  1,  2]))
    # Edge case: the nan-sized chunks resolve to size 0
    a = da.zeros(5, chunks=chunks)
    assert_eq(a[a.nonzero()], np.array([]))
