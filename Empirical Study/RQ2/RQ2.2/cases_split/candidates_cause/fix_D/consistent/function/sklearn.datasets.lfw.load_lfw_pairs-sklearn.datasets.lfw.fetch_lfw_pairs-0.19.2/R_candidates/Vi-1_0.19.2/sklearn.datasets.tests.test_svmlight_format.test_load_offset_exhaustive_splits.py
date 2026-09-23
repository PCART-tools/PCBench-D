def test_load_offset_exhaustive_splits():
    rng = np.random.RandomState(0)
    X = np.array([
        [0, 0, 0, 0, 0, 0],
        [1, 2, 3, 4, 0, 6],
        [1, 2, 3, 4, 0, 6],
        [0, 0, 0, 0, 0, 0],
        [1, 0, 3, 0, 0, 0],
        [0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0],
    ])
    X = sp.csr_matrix(X)
    n_samples, n_features = X.shape
    y = rng.randint(low=0, high=2, size=n_samples)
    query_id = np.arange(n_samples) // 2

    f = BytesIO()
    dump_svmlight_file(X, y, f, query_id=query_id)
    f.seek(0)

    size = len(f.getvalue())

    # load the same data in 2 parts with all the possible byte offsets to
    # locate the split so has to test for particular boundary cases
    for mark in range(size):
        if sp_version < (0, 14) and (mark == 0 or mark > size - 100):
            # old scipy does not support sparse matrices with 0 rows.
            continue
        f.seek(0)
        X_0, y_0, q_0 = load_svmlight_file(f, n_features=n_features,
                                           query_id=True, offset=0,
                                           length=mark)
        X_1, y_1, q_1 = load_svmlight_file(f, n_features=n_features,
                                           query_id=True, offset=mark,
                                           length=-1)
        q_concat = np.concatenate([q_0, q_1])
        y_concat = np.concatenate([y_0, y_1])
        X_concat = sp.vstack([X_0, X_1])
        assert_array_equal(y, y_concat)
        assert_array_equal(query_id, q_concat)
        assert_array_almost_equal(X.toarray(), X_concat.toarray())
