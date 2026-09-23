@pytest.mark.parametrize('dtype', ['int8', 'int16', 'int32', 'int64',
                                   'uint8', 'uint16', 'uint32', 'uint64'])
def test_index_with_int_dask_array_dtypes(dtype):
    a = da.from_array([10, 20, 30, 40], chunks=-1)
    idx = da.from_array(np.array([1, 2]).astype(dtype), chunks=1)
    assert_eq(a[idx], np.array([20, 30]))
