def test_logsumexp_b_shape():
    a = np.zeros((4,1,2,1))
    b = np.ones((3,1,5))

    logsumexp(a, b=b)
