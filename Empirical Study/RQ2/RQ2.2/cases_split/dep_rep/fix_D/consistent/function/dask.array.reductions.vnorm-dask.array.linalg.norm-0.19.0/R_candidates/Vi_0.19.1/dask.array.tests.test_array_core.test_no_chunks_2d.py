def test_no_chunks_2d():
    X = np.arange(24).reshape((4, 6))
    x = da.from_array(X, chunks=(2, 2))
    x._chunks = ((np.nan, np.nan), (np.nan, np.nan, np.nan))

    with pytest.warns(None):  # zero division warning
        assert_eq(da.log(x), np.log(X))
    assert_eq(x.T, X.T)
    assert_eq(x.sum(axis=0, keepdims=True), X.sum(axis=0, keepdims=True))
    assert_eq(x.sum(axis=1, keepdims=True), X.sum(axis=1, keepdims=True))
    assert_eq(x.dot(x.T + 1), X.dot(X.T + 1))
