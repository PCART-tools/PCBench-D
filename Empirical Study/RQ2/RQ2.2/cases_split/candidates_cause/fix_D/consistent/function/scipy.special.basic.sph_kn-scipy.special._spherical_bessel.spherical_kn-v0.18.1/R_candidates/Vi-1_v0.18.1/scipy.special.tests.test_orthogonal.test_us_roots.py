def test_us_roots():
    weightf = orth.sh_chebyu(5).weight_func
    verify_gauss_quad(orth.us_roots, orth.eval_sh_chebyu, weightf, 0., 1., 5)
    verify_gauss_quad(orth.us_roots, orth.eval_sh_chebyu, weightf, 0., 1., 25)
    verify_gauss_quad(orth.us_roots, orth.eval_sh_chebyu, weightf, 0., 1.,
                      100, atol=1e-13)

    x, w = orth.us_roots(5, False)
    y, v, m = orth.us_roots(5, True)
    assert_allclose(x, y, 1e-14, 1e-14)
    assert_allclose(w, v, 1e-14, 1e-14)

    muI, muI_err = integrate.quad(weightf, 0, 1)
    assert_allclose(m, muI, rtol=muI_err)

    assert_raises(ValueError, orth.us_roots, 0)
    assert_raises(ValueError, orth.us_roots, 3.3)
