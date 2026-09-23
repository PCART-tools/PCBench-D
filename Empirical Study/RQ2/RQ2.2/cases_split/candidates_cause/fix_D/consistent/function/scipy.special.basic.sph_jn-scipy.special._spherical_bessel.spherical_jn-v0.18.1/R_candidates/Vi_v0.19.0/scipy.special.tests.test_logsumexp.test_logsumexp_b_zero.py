def test_logsumexp_b_zero():
    a = [1,10000]
    b = [1,0]

    assert_almost_equal(logsumexp(a, b=b), 1)
