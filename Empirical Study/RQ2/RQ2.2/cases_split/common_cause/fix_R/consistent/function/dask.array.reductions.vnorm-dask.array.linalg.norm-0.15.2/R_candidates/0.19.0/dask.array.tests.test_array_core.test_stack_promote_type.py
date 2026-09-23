def test_stack_promote_type():
    i = np.arange(10, dtype='i4')
    f = np.arange(10, dtype='f4')
    di = da.from_array(i, chunks=5)
    df = da.from_array(f, chunks=5)
    res = da.stack([di, df])
    assert_eq(res, np.stack([i, f]))
