@pytest.mark.parametrize("start,stop,step,dtype", [
    (0, 1, 1, None),  # int64
    (1.5, 2, 1, None),  # float64
    (1, 2.5, 1, None),  # float64
    (1, 2, .5, None),  # float64
    (np.float32(1), np.float32(2), np.float32(1), None),  # promoted to float64
    (np.int32(1), np.int32(2), np.int32(1), None),  # promoted to int64
    (np.uint32(1), np.uint32(2), np.uint32(1), None),  # promoted to int64
    (np.uint64(1), np.uint64(2), np.uint64(1), None),  # promoted to float64
    (np.uint32(1), np.uint32(2), np.uint32(1), np.uint32),
    (np.uint64(1), np.uint64(2), np.uint64(1), np.uint64),
    # numpy.arange gives unexpected results
    # https://github.com/numpy/numpy/issues/11505
    # (1j, 2, 1, None),
    # (1, 2j, 1, None),
    # (1, 2, 1j, None),
    # (1+2j, 2+3j, 1+.1j, None),
])
def test_arange_dtypes(start, stop, step, dtype):
    a_np = np.arange(start, stop, step, dtype=dtype)
    a_da = da.arange(start, stop, step, dtype=dtype, chunks=-1)
    assert_eq(a_np, a_da)
