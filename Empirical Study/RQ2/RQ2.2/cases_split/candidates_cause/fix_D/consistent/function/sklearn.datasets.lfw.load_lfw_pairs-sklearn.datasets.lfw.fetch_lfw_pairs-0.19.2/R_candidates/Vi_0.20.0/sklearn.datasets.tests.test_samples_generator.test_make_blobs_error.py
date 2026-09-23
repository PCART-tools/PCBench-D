def test_make_blobs_error():
    n_samples = [20, 20, 20]
    centers = np.array([[0.0, 0.0], [1.0, 1.0], [0.0, 1.0]])
    cluster_stds = np.array([0.05, 0.2, 0.4])
    wrong_centers_msg = ("Length of `n_samples` not consistent "
                         "with number of centers. Got n_samples = {} "
                         "and centers = {}".format(n_samples, centers[:-1]))
    assert_raise_message(ValueError, wrong_centers_msg,
                         make_blobs, n_samples, centers=centers[:-1])
    wrong_std_msg = ("Length of `clusters_std` not consistent with "
                     "number of centers. Got centers = {} "
                     "and cluster_std = {}".format(centers, cluster_stds[:-1]))
    assert_raise_message(ValueError, wrong_std_msg,
                         make_blobs, n_samples,
                         centers=centers, cluster_std=cluster_stds[:-1])
    wrong_type_msg = ("Parameter `centers` must be array-like. "
                      "Got {!r} instead".format(3))
    assert_raise_message(ValueError, wrong_type_msg,
                         make_blobs, n_samples, centers=3)
