def test_gsl():
    TESTS = [
        data_gsl(mathieu_a, 'mathieu_ab', (0, 1), 2, rtol=1e-13, atol=1e-13),
        data_gsl(mathieu_b, 'mathieu_ab', (0, 1), 3, rtol=1e-13, atol=1e-13),

        # Also the GSL output has limited accuracy...
        data_gsl(mathieu_ce_rad, 'mathieu_ce_se', (0, 1, 2), 3, rtol=1e-7, atol=1e-13),
        data_gsl(mathieu_se_rad, 'mathieu_ce_se', (0, 1, 2), 4, rtol=1e-7, atol=1e-13),

        data_gsl(mathieu_mc1_scaled, 'mathieu_mc_ms', (0, 1, 2), 3, rtol=1e-7, atol=1e-13),
        data_gsl(mathieu_ms1_scaled, 'mathieu_mc_ms', (0, 1, 2), 4, rtol=1e-7, atol=1e-13),

        data_gsl(mathieu_mc2_scaled, 'mathieu_mc_ms', (0, 1, 2), 5, rtol=1e-7, atol=1e-13),
        data_gsl(mathieu_ms2_scaled, 'mathieu_mc_ms', (0, 1, 2), 6, rtol=1e-7, atol=1e-13),
    ]

    for test in TESTS:
        yield _test_factory, test
