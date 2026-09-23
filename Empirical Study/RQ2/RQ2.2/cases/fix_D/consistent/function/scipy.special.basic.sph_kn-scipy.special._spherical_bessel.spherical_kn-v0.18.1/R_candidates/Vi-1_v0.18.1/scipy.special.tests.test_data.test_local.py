def test_local():
    TESTS = [
        data_local(ellipkinc, 'ellipkinc_neg_m', (0, 1), 2),
        data_local(ellipkm1, 'ellipkm1', 0, 1),
        data_local(ellipeinc, 'ellipeinc_neg_m', (0, 1), 2),
        data_local(clog1p, 'log1p_expm1_complex', (0,1), (2,3), rtol=1e-14),
        data_local(cexpm1, 'log1p_expm1_complex', (0,1), (4,5), rtol=1e-14),
        data_local(gammainc, 'gammainc', (0, 1), 2, rtol=5e-9),
    ]

    for test in TESTS:
        yield _test_factory, test

    TESTS = [
        data_local(ellip_harm_2, 'ellip',(0, 1, 2, 3, 4), 6, rtol=1e-10, atol=1e-13),
        data_local(ellip_harm, 'ellip',(0, 1, 2, 3, 4), 5, rtol=1e-10, atol=1e-13),
    ]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=IntegrationWarning)

        for test in TESTS:
            yield _test_factory, test

    # sph_jn, sph_yn are deprecated; silence the DeprecationWarning noise 
    TESTS_DEP = [
        data(sph_jn_, 'sph_bessel_data_ipp-sph_bessel_data', (0,1), 2,
            vectorized=False,
            knownfailure='sph_jn inaccurate at large n, small x'),
        data(sph_yn_, 'sph_neumann_data_ipp-sph_neumann_data', (0,1), 2,
            rtol=4e-15, vectorized=False),
    ]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=DeprecationWarning)
        for test in TESTS_DEP:
            yield _test_factory, test
