def test_u_roots():
    weightf = orth.chebyu(5).weight_func
    verify_gauss_quad(orth.u_roots, orth.eval_chebyu, weightf, -1., 1., 5)
    verify_gauss_quad(orth.u_roots, orth.eval_chebyu, weightf, -1., 1., 25)
    verify_gauss_quad(orth.u_roots, orth.eval_chebyu, weightf, -1., 1., 100)

    x, w = orth.u_roots(5, False)
    y, v, m = orth.u_roots(5, True)
    assert_allclose(x, y, 1e-14, 1e-14)
    assert_allclose(w, v, 1e-14, 1e-14)

    muI, muI_err = integrate.quad(weightf, -1, 1)
    assert_allclose(m, muI, rtol=muI_err)

    assert_raises(ValueError, orth.u_roots, 0)
    assert_raises(ValueError, orth.u_roots, 3.3)
