@pytest.mark.parametrize("arr, expected", [
    # array of floats with some nans
    (np.array([np.nan, 5.0, np.nan, np.inf]),
     np.array([False, True, False, True])),
    # int64 array that can't possibly have nans
    (np.array([1, 5, 7, 9], dtype=np.int64),
     True),
    # bool array that can't possibly have nans
    (np.array([False, True, False, True]),
     True),
    # 2-D complex array with nans
    (np.array([[np.nan, 5.0],
               [np.nan, np.inf]], dtype=np.complex64),
     np.array([[False, True],
               [False, True]])),
    ])
def test__nan_mask(arr, expected):
    for out in [None, np.empty(arr.shape, dtype=np.bool_)]:
        actual = _nan_mask(arr, out=out)
        assert_equal(actual, expected)
        # the above won't distinguish between True proper
        # and an array of True values; we want True proper
        # for types that can't possibly contain NaN
        if type(expected) is not np.ndarray:
            assert actual is True
