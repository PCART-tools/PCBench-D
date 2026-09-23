def test_he_roots():
    rootf = orth.he_roots
    evalf = orth.eval_hermitenorm
    weightf = orth.hermitenorm(5).weight_func

    verify_gauss_quad(rootf, evalf, weightf, -np.inf, np.inf, 5)
    verify_gauss_quad(rootf, evalf, weightf, -np.inf, np.inf, 25, atol=1e-13)
    verify_gauss_quad(rootf, evalf, weightf, -np.inf, np.inf, 100, atol=1e-12)

    x, w = orth.he_roots(5, False)
    y, v, m = orth.he_roots(5, True)
    assert_allclose(x, y, 1e-14, 1e-14)
    assert_allclose(w, v, 1e-14, 1e-14)

    muI, muI_err = integrate.quad(weightf, -np.inf, np.inf)
    assert_allclose(m, muI, rtol=muI_err)

    assert_raises(ValueError, orth.he_roots, 0)
    assert_raises(ValueError, orth.he_roots, 3.3)
