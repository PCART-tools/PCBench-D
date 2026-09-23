@pytest.mark.parametrize('sparsity', [0, 0.1, .5, 0.99, 1])
@pytest.mark.parametrize('n_samples', [13, 101])
@pytest.mark.parametrize('n_features', [2, 7, 41])
def test_load_with_offsets(sparsity, n_samples, n_features):
    rng = np.random.RandomState(0)
    X = rng.uniform(low=0.0, high=1.0, size=(n_samples, n_features))
    if sparsity:
        X[X < sparsity] = 0.0
    X = sp.csr_matrix(X)
    y = rng.randint(low=0, high=2, size=n_samples)

    f = BytesIO()
    dump_svmlight_file(X, y, f)
    f.seek(0)

    size = len(f.getvalue())

    # put some marks that are likely to happen anywhere in a row
    mark_0 = 0
    mark_1 = size // 3
    length_0 = mark_1 - mark_0
    mark_2 = 4 * size // 5
    length_1 = mark_2 - mark_1

    # load the original sparse matrix into 3 independent CSR matrices
    X_0, y_0 = load_svmlight_file(f, n_features=n_features,
                                  offset=mark_0, length=length_0)
    X_1, y_1 = load_svmlight_file(f, n_features=n_features,
                                  offset=mark_1, length=length_1)
    X_2, y_2 = load_svmlight_file(f, n_features=n_features,
                                  offset=mark_2)

    y_concat = np.concatenate([y_0, y_1, y_2])
    X_concat = sp.vstack([X_0, X_1, X_2])
    assert_array_almost_equal(y, y_concat)
    assert_array_almost_equal(X.toarray(), X_concat.toarray())
