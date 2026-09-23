def test_make_biclusters():
    X, rows, cols = make_biclusters(
        shape=(100, 100), n_clusters=4, shuffle=True, random_state=0)
    assert_equal(X.shape, (100, 100), "X shape mismatch")
    assert_equal(rows.shape, (4, 100), "rows shape mismatch")
    assert_equal(cols.shape, (4, 100,), "columns shape mismatch")
    assert_all_finite(X)
    assert_all_finite(rows)
    assert_all_finite(cols)

    X2, _, _ = make_biclusters(shape=(100, 100), n_clusters=4,
                               shuffle=True, random_state=0)
    assert_array_almost_equal(X, X2)
