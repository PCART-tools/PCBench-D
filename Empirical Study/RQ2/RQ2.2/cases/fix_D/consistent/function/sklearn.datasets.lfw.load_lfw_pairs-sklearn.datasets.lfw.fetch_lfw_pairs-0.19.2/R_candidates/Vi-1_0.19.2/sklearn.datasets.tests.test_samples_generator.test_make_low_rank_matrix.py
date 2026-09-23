def test_make_low_rank_matrix():
    X = make_low_rank_matrix(n_samples=50, n_features=25, effective_rank=5,
                             tail_strength=0.01, random_state=0)

    assert_equal(X.shape, (50, 25), "X shape mismatch")

    from numpy.linalg import svd
    u, s, v = svd(X)
    assert_less(sum(s) - 5, 0.1, "X rank is not approximately 5")
