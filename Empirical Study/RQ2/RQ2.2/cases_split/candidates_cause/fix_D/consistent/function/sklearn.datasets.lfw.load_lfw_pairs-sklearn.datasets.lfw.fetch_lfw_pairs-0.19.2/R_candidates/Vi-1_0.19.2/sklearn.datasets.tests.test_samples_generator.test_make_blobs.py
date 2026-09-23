def test_make_blobs():
    cluster_stds = np.array([0.05, 0.2, 0.4])
    cluster_centers = np.array([[0.0, 0.0], [1.0, 1.0], [0.0, 1.0]])
    X, y = make_blobs(random_state=0, n_samples=50, n_features=2,
                      centers=cluster_centers, cluster_std=cluster_stds)

    assert_equal(X.shape, (50, 2), "X shape mismatch")
    assert_equal(y.shape, (50,), "y shape mismatch")
    assert_equal(np.unique(y).shape, (3,), "Unexpected number of blobs")
    for i, (ctr, std) in enumerate(zip(cluster_centers, cluster_stds)):
        assert_almost_equal((X[y == i] - ctr).std(), std, 1, "Unexpected std")
