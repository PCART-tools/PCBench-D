def test_binomtest():
    # precision tests compared to R for ticket:986
    pp = np.concatenate((np.linspace(0.1,0.2,5), np.linspace(0.45,0.65,5),
                          np.linspace(0.85,0.95,5)))
    n = 501
    x = 450
    results = [0.0, 0.0, 1.0159969301994141e-304,
    2.9752418572150531e-275, 7.7668382922535275e-250,
    2.3381250925167094e-099, 7.8284591587323951e-081,
    9.9155947819961383e-065, 2.8729390725176308e-050,
    1.7175066298388421e-037, 0.0021070691951093692,
    0.12044570587262322, 0.88154763174802508, 0.027120993063129286,
    2.6102587134694721e-006]

    for p, res in zip(pp,results):
        assert_approx_equal(stats.binom_test(x, n, p), res,
                            significant=12, err_msg='fail forp=%f' % p)

    assert_approx_equal(stats.binom_test(50,100,0.1), 5.8320387857343647e-024,
                            significant=12, err_msg='fail forp=%f' % p)
