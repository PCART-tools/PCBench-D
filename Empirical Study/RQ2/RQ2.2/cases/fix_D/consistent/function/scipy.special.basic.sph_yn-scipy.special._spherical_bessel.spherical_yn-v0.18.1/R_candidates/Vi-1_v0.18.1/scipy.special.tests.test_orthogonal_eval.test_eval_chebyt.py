def test_eval_chebyt():
    n = np.arange(0, 10000, 7)
    x = 2*np.random.rand() - 1
    v1 = np.cos(n*np.arccos(x))
    v2 = orth.eval_chebyt(n, x)
    assert_(np.allclose(v1, v2, rtol=1e-15))
