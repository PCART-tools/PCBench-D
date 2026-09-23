def test_roots_gegenbauer():
    rootf = lambda a: lambda n, mu: sc.roots_gegenbauer(n, a, mu)
    evalf = lambda a: lambda n, x: orth.eval_gegenbauer(n, a, x)
    weightf = lambda a: lambda x: (1 - x**2)**(a - 0.5)

    vgq = verify_gauss_quad
    vgq(rootf(-0.25), evalf(-0.25), weightf(-0.25), -1., 1., 5)
    vgq(rootf(-0.25), evalf(-0.25), weightf(-0.25), -1., 1., 25, atol=1e-12)
    vgq(rootf(-0.25), evalf(-0.25), weightf(-0.25), -1., 1., 100, atol=1e-11)

    vgq(rootf(0.1), evalf(0.1), weightf(0.1), -1., 1., 5)
    vgq(rootf(0.1), evalf(0.1), weightf(0.1), -1., 1., 25, atol=1e-13)
    vgq(rootf(0.1), evalf(0.1), weightf(0.1), -1., 1., 100, atol=1e-12)

    vgq(rootf(1), evalf(1), weightf(1), -1., 1., 5)
    vgq(rootf(1), evalf(1), weightf(1), -1., 1., 25, atol=1e-13)
    vgq(rootf(1), evalf(1), weightf(1), -1., 1., 100, atol=1e-12)

    vgq(rootf(10), evalf(10), weightf(10), -1., 1., 5)
    vgq(rootf(10), evalf(10), weightf(10), -1., 1., 25, atol=1e-13)
    vgq(rootf(10), evalf(10), weightf(10), -1., 1., 100, atol=1e-12)

    vgq(rootf(50), evalf(50), weightf(50), -1., 1., 5, atol=1e-13)
    vgq(rootf(50), evalf(50), weightf(50), -1., 1., 25, atol=1e-12)
    vgq(rootf(50), evalf(50), weightf(50), -1., 1., 100, atol=1e-11)

    # this is a special case that the old code supported.
    # when alpha = 0, the gegenbauer polynomial is uniformly 0. but it goes
    # to a scaled down copy of T_n(x) there.
    vgq(rootf(0), orth.eval_chebyt, weightf(0), -1., 1., 5)
    vgq(rootf(0), orth.eval_chebyt, weightf(0), -1., 1., 25)
    vgq(rootf(0), orth.eval_chebyt, weightf(0), -1., 1., 100)

    x, w = sc.roots_gegenbauer(5, 2, False)
    y, v, m = sc.roots_gegenbauer(5, 2, True)
    assert_allclose(x, y, 1e-14, 1e-14)
    assert_allclose(w, v, 1e-14, 1e-14)

    muI, muI_err = integrate.quad(weightf(2), -1, 1)
    assert_allclose(m, muI, rtol=muI_err)

    assert_raises(ValueError, sc.roots_gegenbauer, 0, 2)
    assert_raises(ValueError, sc.roots_gegenbauer, 3.3, 2)
    assert_raises(ValueError, sc.roots_gegenbauer, 3, -.75)
