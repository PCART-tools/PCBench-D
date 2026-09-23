def test_ps_roots():
    weightf = orth.sh_legendre(5).weight_func
    verify_gauss_quad(orth.ps_roots, orth.eval_sh_legendre, weightf, 0., 1., 5)
    verify_gauss_quad(orth.ps_roots, orth.eval_sh_legendre, weightf, 0., 1.,
                      25, atol=1e-13)
    verify_gauss_quad(orth.ps_roots, orth.eval_sh_legendre, weightf, 0., 1.,
                      100, atol=1e-12)

    x, w = orth.ps_roots(5, False)
    y, v, m = orth.ps_roots(5, True)
    assert_allclose(x, y, 1e-14, 1e-14)
    assert_allclose(w, v, 1e-14, 1e-14)

    muI, muI_err = integrate.quad(weightf, 0, 1)
    assert_allclose(m, muI, rtol=muI_err)

    assert_raises(ValueError, orth.ps_roots, 0)
    assert_raises(ValueError, orth.ps_roots, 3.3)
