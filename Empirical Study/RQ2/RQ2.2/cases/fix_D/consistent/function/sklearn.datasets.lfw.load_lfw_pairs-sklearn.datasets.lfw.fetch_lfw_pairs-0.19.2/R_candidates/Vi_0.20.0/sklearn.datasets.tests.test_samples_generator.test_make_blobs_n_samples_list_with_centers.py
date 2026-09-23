def test_make_blobs_n_samples_list_with_centers():
    n_samples = [20, 20, 20]
    centers = np.array([[0.0, 0.0], [1.0, 1.0], [0.0, 1.0]])
    cluster_stds = np.array([0.05, 0.2, 0.4])
    X, y = make_blobs(n_samples=n_samples, centers=centers,
                      cluster_std=cluster_stds, random_state=0)

    assert X.shape == (sum(n_samples), 2), "X shape mismatch"
    assert all(np.bincount(y, minlength=len(n_samples)) == n_samples), \
        "Incorrect number of samples per blob"
    for i, (ctr, std) in enumerate(zip(centers, cluster_stds)):
        assert_almost_equal((X[y == i] - ctr).std(), std, 1, "Unexpected std")
