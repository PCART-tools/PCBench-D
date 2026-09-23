@pytest.mark.parametrize('chunks', [2, 4])
def test_index_with_int_dask_array_negindex(chunks):
    a = da.arange(4, chunks=chunks)
    idx = da.from_array([-1, -4], chunks=1)
    assert_eq(a[idx], np.array([3, 0]))
