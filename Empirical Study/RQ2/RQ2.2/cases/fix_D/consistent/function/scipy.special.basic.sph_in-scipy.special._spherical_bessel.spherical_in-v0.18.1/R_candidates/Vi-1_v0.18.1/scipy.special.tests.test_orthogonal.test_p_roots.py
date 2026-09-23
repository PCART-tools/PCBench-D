def test_p_roots():
    weightf = orth.legendre(5).weight_func
    verify_gauss_quad(orth.p_roots, orth.eval_legendre, weightf, -1., 1., 5)
    verify_gauss_quad(orth.p_roots, orth.eval_legendre, weightf, -1., 1.,
                      25, atol=1e-13)
    verify_gauss_quad(orth.p_roots, orth.eval_legendre, weightf, -1., 1.,
                      100, atol=1e-12)

    x, w = orth.p_roots(5, False)
    y, v, m = orth.p_roots(5, True)
    assert_allclose(x, y, 1e-14, 1e-14)
    assert_allclose(w, v, 1e-14, 1e-14)

    muI, muI_err = integrate.quad(weightf, -1, 1)
    assert_allclose(m, muI, rtol=muI_err)

    assert_raises(ValueError, orth.p_roots, 0)
    assert_raises(ValueError, orth.p_roots, 3.3)
