def test_make_checkerboard():
    X, rows, cols = make_checkerboard(
        shape=(100, 100), n_clusters=(20, 5),
        shuffle=True, random_state=0)
    assert_equal(X.shape, (100, 100), "X shape mismatch")
    assert_equal(rows.shape, (100, 100), "rows shape mismatch")
    assert_equal(cols.shape, (100, 100,), "columns shape mismatch")

    X, rows, cols = make_checkerboard(
        shape=(100, 100), n_clusters=2, shuffle=True, random_state=0)
    assert_all_finite(X)
    assert_all_finite(rows)
    assert_all_finite(cols)

    X1, _, _ = make_checkerboard(shape=(100, 100), n_clusters=2,
                                 shuffle=True, random_state=0)
    X2, _, _ = make_checkerboard(shape=(100, 100), n_clusters=2,
                                 shuffle=True, random_state=0)
    assert_array_almost_equal(X1, X2)
