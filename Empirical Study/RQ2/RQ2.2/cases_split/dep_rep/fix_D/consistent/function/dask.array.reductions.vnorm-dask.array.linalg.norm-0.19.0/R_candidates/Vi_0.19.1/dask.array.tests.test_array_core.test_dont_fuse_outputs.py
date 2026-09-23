def test_dont_fuse_outputs():
    dsk = {('x', 0): np.array([1, 2]),
           ('x', 1): (inc, ('x', 0))}

    a = da.Array(dsk, 'x', chunks=(2,), shape=(4,), dtype=np.array([1]).dtype)
    assert_eq(a, np.array([1, 2, 2, 3], dtype=a.dtype))
