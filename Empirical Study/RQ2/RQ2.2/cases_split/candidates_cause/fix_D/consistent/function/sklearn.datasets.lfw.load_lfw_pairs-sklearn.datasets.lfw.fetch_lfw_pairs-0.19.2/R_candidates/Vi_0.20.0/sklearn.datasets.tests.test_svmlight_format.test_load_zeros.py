def test_load_zeros():
    f = BytesIO()
    true_X = sp.csr_matrix(np.zeros(shape=(3, 4)))
    true_y = np.array([0, 1, 0])
    dump_svmlight_file(true_X, true_y, f)

    for zero_based in ['auto', True, False]:
        f.seek(0)
        X, y = load_svmlight_file(f, n_features=4, zero_based=zero_based)
        assert_array_almost_equal(y, true_y)
        assert_array_almost_equal(X.toarray(), true_X.toarray())
