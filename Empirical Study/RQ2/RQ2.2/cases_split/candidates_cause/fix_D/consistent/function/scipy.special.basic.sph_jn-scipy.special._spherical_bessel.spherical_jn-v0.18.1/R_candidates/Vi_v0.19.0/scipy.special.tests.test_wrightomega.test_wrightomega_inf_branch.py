def test_wrightomega_inf_branch():
    pts = [complex(-np.inf, np.pi/4),
           complex(-np.inf, -np.pi/4),
           complex(-np.inf, 3*np.pi/4),
           complex(-np.inf, -3*np.pi/4)]
    for p in pts:
        res = sc.wrightomega(p)
        assert_equal(res, 0)
        if abs(p.imag) <= np.pi/2:
            assert_(np.signbit(res.real) == False)
        else:
            assert_(np.signbit(res.real) == True)
        if p.imag >= 0:
            assert_(np.signbit(res.imag) == False)
        else:
            assert_(np.signbit(res.imag) == True)
