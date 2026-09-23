def test_t_roots():
    weightf = orth.chebyt(5).weight_func
    verify_gauss_quad(orth.t_roots, orth.eval_chebyt, weightf, -1., 1., 5)
    verify_gauss_quad(orth.t_roots, orth.eval_chebyt, weightf, -1., 1., 25)
    verify_gauss_quad(orth.t_roots, orth.eval_chebyt, weightf, -1., 1., 100)

    x, w = orth.t_roots(5, False)
    y, v, m = orth.t_roots(5, True)
    assert_allclose(x, y, 1e-14, 1e-14)
    assert_allclose(w, v, 1e-14, 1e-14)

    muI, muI_err = integrate.quad(weightf, -1, 1)
    assert_allclose(m, muI, rtol=muI_err)

    assert_raises(ValueError, orth.t_roots, 0)
    assert_raises(ValueError, orth.t_roots, 3.3)
