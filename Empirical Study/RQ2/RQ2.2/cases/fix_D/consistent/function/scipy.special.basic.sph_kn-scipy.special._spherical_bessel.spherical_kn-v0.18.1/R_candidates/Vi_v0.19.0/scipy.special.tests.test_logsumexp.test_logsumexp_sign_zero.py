def test_logsumexp_sign_zero():
    a = [1,1]
    b = [1,-1]

    r, s = logsumexp(a, b=b, return_sign=True)
    assert_(not np.isfinite(r))
    assert_(not np.isnan(r))
    assert_(r < 0)
    assert_equal(s,0)
