def test_l_roots():
    weightf = orth.laguerre(5).weight_func
    verify_gauss_quad(orth.l_roots, orth.eval_laguerre, weightf, 0., np.inf, 5)
    verify_gauss_quad(orth.l_roots, orth.eval_laguerre, weightf, 0., np.inf,
                      25, atol=1e-13)
    verify_gauss_quad(orth.l_roots, orth.eval_laguerre, weightf, 0., np.inf,
                      100, atol=1e-12)

    x, w = orth.l_roots(5, False)
    y, v, m = orth.l_roots(5, True)
    assert_allclose(x, y, 1e-14, 1e-14)
    assert_allclose(w, v, 1e-14, 1e-14)

    muI, muI_err = integrate.quad(weightf, 0, np.inf)
    assert_allclose(m, muI, rtol=muI_err)

    assert_raises(ValueError, orth.l_roots, 0)
    assert_raises(ValueError, orth.l_roots, 3.3)
