def test_dont_dealias_outputs():
    dsk = {('x', 0, 0): np.ones((2, 2)),
           ('x', 0, 1): np.ones((2, 2)),
           ('x', 1, 0): np.ones((2, 2)),
           ('x', 1, 1): ('x', 0, 0)}

    a = da.Array(dsk, 'x', chunks=(2, 2), shape=(4, 4), dtype=np.ones(1).dtype)
    assert_eq(a, np.ones((4, 4)))
