def test_c_roots():
    weightf = orth.chebyc(5).weight_func
    verify_gauss_quad(orth.c_roots, orth.eval_chebyc, weightf, -2., 2., 5)
    verify_gauss_quad(orth.c_roots, orth.eval_chebyc, weightf, -2., 2., 25)
    verify_gauss_quad(orth.c_roots, orth.eval_chebyc, weightf, -2., 2., 100)

    x, w = orth.c_roots(5, False)
    y, v, m = orth.c_roots(5, True)
    assert_allclose(x, y, 1e-14, 1e-14)
    assert_allclose(w, v, 1e-14, 1e-14)

    muI, muI_err = integrate.quad(weightf, -2, 2)
    assert_allclose(m, muI, rtol=muI_err)

    assert_raises(ValueError, orth.c_roots, 0)
    assert_raises(ValueError, orth.c_roots, 3.3)
