def test_no_chunks_yes_chunks():
    X = np.arange(24).reshape((4, 6))
    x = da.from_array(X, chunks=(2, 2))
    x._chunks = ((2, 2), (np.nan, np.nan, np.nan))

    assert (x + 1).chunks == ((2, 2), (np.nan, np.nan, np.nan))
    assert (x.T).chunks == ((np.nan, np.nan, np.nan), (2, 2))
    assert (x.dot(x.T)).chunks == ((2, 2), (2, 2))
