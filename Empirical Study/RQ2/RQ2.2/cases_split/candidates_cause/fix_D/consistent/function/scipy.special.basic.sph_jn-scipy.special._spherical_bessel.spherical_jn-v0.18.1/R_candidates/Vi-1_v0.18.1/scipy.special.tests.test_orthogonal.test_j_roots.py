def test_j_roots():
    rf = lambda a, b: lambda n, mu: orth.j_roots(n, a, b, mu)
    ef = lambda a, b: lambda n, x: orth.eval_jacobi(n, a, b, x)
    wf = lambda a, b: lambda x: (1 - x)**a * (1 + x)**b

    vgq = verify_gauss_quad
    vgq(rf(-0.5, -0.75), ef(-0.5, -0.75), wf(-0.5, -0.75), -1., 1., 5)
    vgq(rf(-0.5, -0.75), ef(-0.5, -0.75), wf(-0.5, -0.75), -1., 1.,
        25, atol=1e-12)
    vgq(rf(-0.5, -0.75), ef(-0.5, -0.75), wf(-0.5, -0.75), -1., 1.,
        100, atol=1e-11)

    vgq(rf(0.5, -0.5), ef(0.5, -0.5), wf(0.5, -0.5), -1., 1., 5)
    vgq(rf(0.5, -0.5), ef(0.5, -0.5), wf(0.5, -0.5), -1., 1., 25, atol=1.5e-13)
    vgq(rf(0.5, -0.5), ef(0.5, -0.5), wf(0.5, -0.5), -1., 1., 100, atol=1e-12)

    vgq(rf(1, 0.5), ef(1, 0.5), wf(1, 0.5), -1., 1., 5, atol=2e-13)
    vgq(rf(1, 0.5), ef(1, 0.5), wf(1, 0.5), -1., 1., 25, atol=2e-13)
    vgq(rf(1, 0.5), ef(1, 0.5), wf(1, 0.5), -1., 1., 100, atol=1e-12)

    vgq(rf(0.9, 2), ef(0.9, 2), wf(0.9, 2), -1., 1., 5)
    vgq(rf(0.9, 2), ef(0.9, 2), wf(0.9, 2), -1., 1., 25, atol=1e-13)
    vgq(rf(0.9, 2), ef(0.9, 2), wf(0.9, 2), -1., 1., 100, atol=2e-13)

    vgq(rf(18.24, 27.3), ef(18.24, 27.3), wf(18.24, 27.3), -1., 1., 5)
    vgq(rf(18.24, 27.3), ef(18.24, 27.3), wf(18.24, 27.3), -1., 1., 25)
    vgq(rf(18.24, 27.3), ef(18.24, 27.3), wf(18.24, 27.3), -1., 1.,
        100, atol=1e-13)

    vgq(rf(47.1, -0.2), ef(47.1, -0.2), wf(47.1, -0.2), -1., 1., 5, atol=1e-13)
    vgq(rf(47.1, -0.2), ef(47.1, -0.2), wf(47.1, -0.2), -1., 1., 25, atol=2e-13)
    vgq(rf(47.1, -0.2), ef(47.1, -0.2), wf(47.1, -0.2), -1., 1.,
        100, atol=1e-11)

    vgq(rf(2.25, 68.9), ef(2.25, 68.9), wf(2.25, 68.9), -1., 1., 5)
    vgq(rf(2.25, 68.9), ef(2.25, 68.9), wf(2.25, 68.9), -1., 1., 25, atol=1e-13)
    vgq(rf(2.25, 68.9), ef(2.25, 68.9), wf(2.25, 68.9), -1., 1.,
        100, atol=1e-13)

    # when alpha == beta == 0, P_n^{a,b}(x) == P_n(x)
    xj, wj = orth.j_roots(6, 0.0, 0.0)
    xl, wl = orth.p_roots(6)
    assert_allclose(xj, xl, 1e-14, 1e-14)
    assert_allclose(wj, wl, 1e-14, 1e-14)

    # when alpha == beta != 0, P_n^{a,b}(x) == C_n^{alpha+0.5}(x)
    xj, wj = orth.j_roots(6, 4.0, 4.0)
    xc, wc = orth.cg_roots(6, 4.5)
    assert_allclose(xj, xc, 1e-14, 1e-14)
    assert_allclose(wj, wc, 1e-14, 1e-14)

    x, w = orth.j_roots(5, 2, 3, False)
    y, v, m = orth.j_roots(5, 2, 3, True)
    assert_allclose(x, y, 1e-14, 1e-14)
    assert_allclose(w, v, 1e-14, 1e-14)

    muI, muI_err = integrate.quad(wf(2,3), -1, 1)
    assert_allclose(m, muI, rtol=muI_err)

    assert_raises(ValueError, orth.j_roots, 0, 1, 1)
    assert_raises(ValueError, orth.j_roots, 3.3, 1, 1)
    assert_raises(ValueError, orth.j_roots, 3, -2, 1)
    assert_raises(ValueError, orth.j_roots, 3, 1, -2)
    assert_raises(ValueError, orth.j_roots, 3, -2, -2)
