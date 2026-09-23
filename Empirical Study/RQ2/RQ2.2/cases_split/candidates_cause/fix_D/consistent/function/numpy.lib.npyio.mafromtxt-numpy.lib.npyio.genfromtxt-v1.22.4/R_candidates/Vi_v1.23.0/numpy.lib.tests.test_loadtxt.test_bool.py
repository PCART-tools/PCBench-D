def test_bool():
    # Simple test for bool via integer
    txt = StringIO("1, 0\n10, -1")
    res = np.loadtxt(txt, dtype=bool, delimiter=",")
    assert res.dtype == bool
    assert_array_equal(res, [[True, False], [True, True]])
    # Make sure we use only 1 and 0 on the byte level:
    assert_array_equal(res.view(np.uint8), [[1, 0], [1, 1]])
