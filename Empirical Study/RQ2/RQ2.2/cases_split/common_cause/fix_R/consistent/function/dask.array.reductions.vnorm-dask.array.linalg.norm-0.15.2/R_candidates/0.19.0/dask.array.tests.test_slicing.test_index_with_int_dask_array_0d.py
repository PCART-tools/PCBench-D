@pytest.mark.parametrize('chunks', [1, 2, 3])
def test_index_with_int_dask_array_0d(chunks):
    # Slice by 0-dimensional array
    x = da.from_array([[10, 20, 30],
                       [40, 50, 60]], chunks=chunks)
    idx0 = da.from_array(1, chunks=1)
    assert_eq(x[idx0, :], x[1, :])
    assert_eq(x[:, idx0], x[:, 1])
