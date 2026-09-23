def test_boost():
    TESTS = [
        data(arccosh, 'acosh_data_ipp-acosh_data', 0, 1, rtol=5e-13),
        data(arccosh, 'acosh_data_ipp-acosh_data', 0j, 1, rtol=5e-13),

        data(arcsinh, 'asinh_data_ipp-asinh_data', 0, 1, rtol=1e-11),
        data(arcsinh, 'asinh_data_ipp-asinh_data', 0j, 1, rtol=1e-11),

        data(arctanh, 'atanh_data_ipp-atanh_data', 0, 1, rtol=1e-11),
        data(arctanh, 'atanh_data_ipp-atanh_data', 0j, 1, rtol=1e-11),

        data(assoc_legendre_p_boost_, 'assoc_legendre_p_ipp-assoc_legendre_p', (0,1,2), 3, rtol=1e-11),

        data(legendre_p_via_assoc_, 'legendre_p_ipp-legendre_p', (0,1), 2, rtol=1e-11),
        data(legendre_p_via_assoc_, 'legendre_p_large_ipp-legendre_p_large', (0,1), 2, rtol=7e-14),
        data(legendre_p_via_lpmn, 'legendre_p_ipp-legendre_p', (0,1), 2, rtol=5e-14, vectorized=False),
        data(legendre_p_via_lpmn, 'legendre_p_large_ipp-legendre_p_large', (0,1), 2, rtol=7e-14, vectorized=False),
        data(lpn_, 'legendre_p_ipp-legendre_p', (0,1), 2, rtol=5e-14, vectorized=False),
        data(lpn_, 'legendre_p_large_ipp-legendre_p_large', (0,1), 2, rtol=3e-13, vectorized=False),
        data(eval_legendre_ld, 'legendre_p_ipp-legendre_p', (0,1), 2, rtol=6e-14),
        data(eval_legendre_ld, 'legendre_p_large_ipp-legendre_p_large', (0,1), 2, rtol=2e-13),
        data(eval_legendre_dd, 'legendre_p_ipp-legendre_p', (0,1), 2, rtol=2e-14),
        data(eval_legendre_dd, 'legendre_p_large_ipp-legendre_p_large', (0,1), 2, rtol=2e-13),

        data(lqn_, 'legendre_p_ipp-legendre_p', (0,1), 3, rtol=2e-14, vectorized=False),
        data(lqn_, 'legendre_p_large_ipp-legendre_p_large', (0,1), 3, rtol=2e-12, vectorized=False),
        data(legendre_q_via_lqmn, 'legendre_p_ipp-legendre_p', (0,1), 3, rtol=2e-14, vectorized=False),
        data(legendre_q_via_lqmn, 'legendre_p_large_ipp-legendre_p_large', (0,1), 3, rtol=2e-12, vectorized=False),

        data(beta, 'beta_exp_data_ipp-beta_exp_data', (0,1), 2, rtol=1e-13),
        data(beta, 'beta_exp_data_ipp-beta_exp_data', (0,1), 2, rtol=1e-13),
        data(beta, 'beta_small_data_ipp-beta_small_data', (0,1), 2),
        data(beta, 'beta_med_data_ipp-beta_med_data', (0,1), 2, rtol=5e-13),

        data(betainc, 'ibeta_small_data_ipp-ibeta_small_data', (0,1,2), 5, rtol=6e-15),
        data(betainc, 'ibeta_data_ipp-ibeta_data', (0,1,2), 5, rtol=5e-13),
        data(betainc, 'ibeta_int_data_ipp-ibeta_int_data', (0,1,2), 5, rtol=2e-14),
        data(betainc, 'ibeta_large_data_ipp-ibeta_large_data', (0,1,2), 5, rtol=4e-10),

        data(betaincinv, 'ibeta_inv_data_ipp-ibeta_inv_data', (0,1,2), 3, rtol=1e-5),

        data(btdtr, 'ibeta_small_data_ipp-ibeta_small_data', (0,1,2), 5, rtol=6e-15),
        data(btdtr, 'ibeta_data_ipp-ibeta_data', (0,1,2), 5, rtol=4e-13),
        data(btdtr, 'ibeta_int_data_ipp-ibeta_int_data', (0,1,2), 5, rtol=2e-14),
        data(btdtr, 'ibeta_large_data_ipp-ibeta_large_data', (0,1,2), 5, rtol=4e-10),

        data(btdtri, 'ibeta_inv_data_ipp-ibeta_inv_data', (0,1,2), 3, rtol=1e-5),
        data(btdtri_comp, 'ibeta_inv_data_ipp-ibeta_inv_data', (0,1,2), 4, rtol=8e-7),

        data(btdtria, 'ibeta_inva_data_ipp-ibeta_inva_data', (2,0,1), 3, rtol=5e-9),
        data(btdtria_comp, 'ibeta_inva_data_ipp-ibeta_inva_data', (2,0,1), 4, rtol=5e-9),

        data(btdtrib, 'ibeta_inva_data_ipp-ibeta_inva_data', (0,2,1), 5, rtol=5e-9),
        data(btdtrib_comp, 'ibeta_inva_data_ipp-ibeta_inva_data', (0,2,1), 6, rtol=5e-9),

        data(binom, 'binomial_data_ipp-binomial_data', (0,1), 2, rtol=1e-13),
        data(binom, 'binomial_large_data_ipp-binomial_large_data', (0,1), 2, rtol=5e-13),

        data(bdtrik, 'binomial_quantile_ipp-binomial_quantile_data', (2,0,1), 3, rtol=5e-9),
        data(bdtrik_comp, 'binomial_quantile_ipp-binomial_quantile_data', (2,0,1), 4, rtol=5e-9),

        data(nbdtrik, 'negative_binomial_quantile_ipp-negative_binomial_quantile_data', (2,0,1), 3, rtol=4e-9),
        data(nbdtrik_comp, 'negative_binomial_quantile_ipp-negative_binomial_quantile_data', (2,0,1), 4, rtol=4e-9),

        data(pdtrik, 'poisson_quantile_ipp-poisson_quantile_data', (1,0), 2, rtol=3e-9),
        data(pdtrik_comp, 'poisson_quantile_ipp-poisson_quantile_data', (1,0), 3, rtol=4e-9),

        data(cbrt, 'cbrt_data_ipp-cbrt_data', 1, 0),

        data(digamma, 'digamma_data_ipp-digamma_data', 0, 1),
        data(digamma, 'digamma_data_ipp-digamma_data', 0j, 1),
        data(digamma, 'digamma_neg_data_ipp-digamma_neg_data', 0, 1, rtol=1e-13),
        data(digamma, 'digamma_neg_data_ipp-digamma_neg_data', 0j, 1, rtol=1e-13),
        data(digamma, 'digamma_root_data_ipp-digamma_root_data', 0, 1, rtol=1e-11),
        data(digamma, 'digamma_root_data_ipp-digamma_root_data', 0j, 1, rtol=1e-11),
        data(digamma, 'digamma_small_data_ipp-digamma_small_data', 0, 1),
        data(digamma, 'digamma_small_data_ipp-digamma_small_data', 0j, 1, rtol=1e-14),

        data(ellipk_, 'ellint_k_data_ipp-ellint_k_data', 0, 1),
        data(ellipkinc_, 'ellint_f_data_ipp-ellint_f_data', (0,1), 2, rtol=1e-14),
        data(ellipe_, 'ellint_e_data_ipp-ellint_e_data', 0, 1),
        data(ellipeinc_, 'ellint_e2_data_ipp-ellint_e2_data', (0,1), 2, rtol=1e-14),

        data(erf, 'erf_data_ipp-erf_data', 0, 1),
        data(erf, 'erf_data_ipp-erf_data', 0j, 1, rtol=1e-13),
        data(erfc, 'erf_data_ipp-erf_data', 0, 2, rtol=6e-15),
        data(erf, 'erf_large_data_ipp-erf_large_data', 0, 1),
        data(erf, 'erf_large_data_ipp-erf_large_data', 0j, 1),
        data(erfc, 'erf_large_data_ipp-erf_large_data', 0, 2, rtol=4e-14),
        data(erf, 'erf_small_data_ipp-erf_small_data', 0, 1),
        data(erf, 'erf_small_data_ipp-erf_small_data', 0j, 1, rtol=1e-13),
        data(erfc, 'erf_small_data_ipp-erf_small_data', 0, 2),

        data(erfinv, 'erf_inv_data_ipp-erf_inv_data', 0, 1),
        data(erfcinv, 'erfc_inv_data_ipp-erfc_inv_data', 0, 1),
        data(erfcinv, 'erfc_inv_big_data_ipp-erfc_inv_big_data2', 0, 1),

        data(exp1, 'expint_1_data_ipp-expint_1_data', 1, 2, rtol=1e-13),
        data(exp1, 'expint_1_data_ipp-expint_1_data', 1j, 2, rtol=5e-9),
        data(expi, 'expinti_data_ipp-expinti_data', 0, 1, rtol=1e-13),
        data(expi, 'expinti_data_double_ipp-expinti_data_double', 0, 1, rtol=1e-13),

        data(expn, 'expint_small_data_ipp-expint_small_data', (0,1), 2),
        data(expn, 'expint_data_ipp-expint_data', (0,1), 2, rtol=1e-14),

        data(gamma, 'test_gamma_data_ipp-near_0', 0, 1),
        data(gamma, 'test_gamma_data_ipp-near_1', 0, 1),
        data(gamma, 'test_gamma_data_ipp-near_2', 0, 1),
        data(gamma, 'test_gamma_data_ipp-near_m10', 0, 1),
        data(gamma, 'test_gamma_data_ipp-near_m55', 0, 1, rtol=7e-12),
        data(gamma, 'test_gamma_data_ipp-factorials', 0, 1, rtol=4e-14),
        data(gamma, 'test_gamma_data_ipp-near_0', 0j, 1, rtol=2e-9),
        data(gamma, 'test_gamma_data_ipp-near_1', 0j, 1, rtol=2e-9),
        data(gamma, 'test_gamma_data_ipp-near_2', 0j, 1, rtol=2e-9),
        data(gamma, 'test_gamma_data_ipp-near_m10', 0j, 1, rtol=2e-9),
        data(gamma, 'test_gamma_data_ipp-near_m55', 0j, 1, rtol=2e-9),
        data(gamma, 'test_gamma_data_ipp-factorials', 0j, 1, rtol=2e-13),
        data(gammaln, 'test_gamma_data_ipp-near_0', 0, 2, rtol=5e-11),
        data(gammaln, 'test_gamma_data_ipp-near_1', 0, 2, rtol=5e-11),
        data(gammaln, 'test_gamma_data_ipp-near_2', 0, 2, rtol=2e-10),
        data(gammaln, 'test_gamma_data_ipp-near_m10', 0, 2, rtol=5e-11),
        data(gammaln, 'test_gamma_data_ipp-near_m55', 0, 2, rtol=5e-11),
        data(gammaln, 'test_gamma_data_ipp-factorials', 0, 2),

        data(gammainc, 'igamma_small_data_ipp-igamma_small_data', (0,1), 5, rtol=5e-15),
        data(gammainc, 'igamma_med_data_ipp-igamma_med_data', (0,1), 5, rtol=2e-13),
        data(gammainc, 'igamma_int_data_ipp-igamma_int_data', (0,1), 5, rtol=2e-13),
        data(gammainc, 'igamma_big_data_ipp-igamma_big_data', (0,1), 5, rtol=1e-12),

        data(gdtr_, 'igamma_small_data_ipp-igamma_small_data', (0,1), 5, rtol=1e-13),
        data(gdtr_, 'igamma_med_data_ipp-igamma_med_data', (0,1), 5, rtol=2e-13),
        data(gdtr_, 'igamma_int_data_ipp-igamma_int_data', (0,1), 5, rtol=2e-13),
        data(gdtr_, 'igamma_big_data_ipp-igamma_big_data', (0,1), 5, rtol=2e-9),

        data(gammaincc, 'igamma_small_data_ipp-igamma_small_data', (0,1), 3, rtol=1e-13),
        data(gammaincc, 'igamma_med_data_ipp-igamma_med_data', (0,1), 3, rtol=2e-13),
        data(gammaincc, 'igamma_int_data_ipp-igamma_int_data', (0,1), 3, rtol=4e-14),
        data(gammaincc, 'igamma_big_data_ipp-igamma_big_data', (0,1), 3, rtol=1e-11),

        data(gdtrc_, 'igamma_small_data_ipp-igamma_small_data', (0,1), 3, rtol=1e-13),
        data(gdtrc_, 'igamma_med_data_ipp-igamma_med_data', (0,1), 3, rtol=2e-13),
        data(gdtrc_, 'igamma_int_data_ipp-igamma_int_data', (0,1), 3, rtol=4e-14),
        data(gdtrc_, 'igamma_big_data_ipp-igamma_big_data', (0,1), 3, rtol=1e-11),

        data(gdtrib_, 'igamma_inva_data_ipp-igamma_inva_data', (1,0), 2, rtol=5e-9),
        data(gdtrib_comp, 'igamma_inva_data_ipp-igamma_inva_data', (1,0), 3, rtol=5e-9),

        data(poch_, 'tgamma_delta_ratio_data_ipp-tgamma_delta_ratio_data', (0,1), 2, rtol=2e-13),
        data(poch_, 'tgamma_delta_ratio_int_ipp-tgamma_delta_ratio_int', (0,1), 2,),
        data(poch_, 'tgamma_delta_ratio_int2_ipp-tgamma_delta_ratio_int2', (0,1), 2,),
        data(poch_minus, 'tgamma_delta_ratio_data_ipp-tgamma_delta_ratio_data', (0,1), 3, rtol=2e-13),
        data(poch_minus, 'tgamma_delta_ratio_int_ipp-tgamma_delta_ratio_int', (0,1), 3),
        data(poch_minus, 'tgamma_delta_ratio_int2_ipp-tgamma_delta_ratio_int2', (0,1), 3),


        data(eval_hermite_ld, 'hermite_ipp-hermite', (0,1), 2, rtol=2e-14),
        data(eval_laguerre_ld, 'laguerre2_ipp-laguerre2', (0,1), 2, rtol=7e-12),
        data(eval_laguerre_dd, 'laguerre2_ipp-laguerre2', (0,1), 2, knownfailure='hyp2f1 insufficiently accurate.'),
        data(eval_genlaguerre_ldd, 'laguerre3_ipp-laguerre3', (0,1,2), 3, rtol=2e-13),
        data(eval_genlaguerre_ddd, 'laguerre3_ipp-laguerre3', (0,1,2), 3, knownfailure='hyp2f1 insufficiently accurate.'),

        data(log1p, 'log1p_expm1_data_ipp-log1p_expm1_data', 0, 1),
        data(expm1, 'log1p_expm1_data_ipp-log1p_expm1_data', 0, 2),

        data(iv, 'bessel_i_data_ipp-bessel_i_data', (0,1), 2, rtol=1e-12),
        data(iv, 'bessel_i_data_ipp-bessel_i_data', (0,1j), 2, rtol=2e-10, atol=1e-306),
        data(iv, 'bessel_i_int_data_ipp-bessel_i_int_data', (0,1), 2, rtol=1e-9),
        data(iv, 'bessel_i_int_data_ipp-bessel_i_int_data', (0,1j), 2, rtol=2e-10),

        data(jn, 'bessel_j_int_data_ipp-bessel_j_int_data', (0,1), 2, rtol=1e-12),
        data(jn, 'bessel_j_int_data_ipp-bessel_j_int_data', (0,1j), 2, rtol=1e-12),
        data(jn, 'bessel_j_large_data_ipp-bessel_j_large_data', (0,1), 2, rtol=6e-11),
        data(jn, 'bessel_j_large_data_ipp-bessel_j_large_data', (0,1j), 2, rtol=6e-11),

        data(jv, 'bessel_j_int_data_ipp-bessel_j_int_data', (0,1), 2, rtol=1e-12),
        data(jv, 'bessel_j_int_data_ipp-bessel_j_int_data', (0,1j), 2, rtol=1e-12),
        data(jv, 'bessel_j_data_ipp-bessel_j_data', (0,1), 2, rtol=1e-12),
        data(jv, 'bessel_j_data_ipp-bessel_j_data', (0,1j), 2, rtol=1e-12),

        data(kn, 'bessel_k_int_data_ipp-bessel_k_int_data', (0,1), 2, rtol=1e-12),

        data(kv, 'bessel_k_int_data_ipp-bessel_k_int_data', (0,1), 2, rtol=1e-12),
        data(kv, 'bessel_k_int_data_ipp-bessel_k_int_data', (0,1j), 2, rtol=1e-12),
        data(kv, 'bessel_k_data_ipp-bessel_k_data', (0,1), 2, rtol=1e-12),
        data(kv, 'bessel_k_data_ipp-bessel_k_data', (0,1j), 2, rtol=1e-12),

        data(yn, 'bessel_y01_data_ipp-bessel_y01_data', (0,1), 2, rtol=1e-12),
        data(yn, 'bessel_yn_data_ipp-bessel_yn_data', (0,1), 2, rtol=1e-12),

        data(yv, 'bessel_yn_data_ipp-bessel_yn_data', (0,1), 2, rtol=1e-12),
        data(yv, 'bessel_yn_data_ipp-bessel_yn_data', (0,1j), 2, rtol=1e-12),
        data(yv, 'bessel_yv_data_ipp-bessel_yv_data', (0,1), 2, rtol=1e-10),
        data(yv, 'bessel_yv_data_ipp-bessel_yv_data', (0,1j), 2, rtol=1e-10),

        data(zeta_, 'zeta_data_ipp-zeta_data', 0, 1, param_filter=(lambda s: s > 1)),
        data(zeta_, 'zeta_neg_data_ipp-zeta_neg_data', 0, 1, param_filter=(lambda s: s > 1)),
        data(zeta_, 'zeta_1_up_data_ipp-zeta_1_up_data', 0, 1, param_filter=(lambda s: s > 1)),
        data(zeta_, 'zeta_1_below_data_ipp-zeta_1_below_data', 0, 1, param_filter=(lambda s: s > 1)),

        data(gammaincinv, 'gamma_inv_small_data_ipp-gamma_inv_small_data', (0,1), 2, rtol=3e-11, knownfailure='gammaincinv bad few small points'),
        data(gammaincinv, 'gamma_inv_data_ipp-gamma_inv_data', (0,1), 2, rtol=1e-12),
        data(gammaincinv, 'gamma_inv_big_data_ipp-gamma_inv_big_data', (0,1), 2, rtol=1e-11),

        data(gammainccinv, 'gamma_inv_small_data_ipp-gamma_inv_small_data', (0,1), 3, rtol=2e-12),
        data(gammainccinv, 'gamma_inv_data_ipp-gamma_inv_data', (0,1), 3, rtol=2e-14),
        data(gammainccinv, 'gamma_inv_big_data_ipp-gamma_inv_big_data', (0,1), 3, rtol=3e-12),

        data(gdtrix_, 'gamma_inv_small_data_ipp-gamma_inv_small_data', (0,1), 2, rtol=3e-13, knownfailure='gdtrix unflow some points'),
        data(gdtrix_, 'gamma_inv_data_ipp-gamma_inv_data', (0,1), 2, rtol=3e-15),
        data(gdtrix_, 'gamma_inv_big_data_ipp-gamma_inv_big_data', (0,1), 2),
        data(gdtrix_comp, 'gamma_inv_small_data_ipp-gamma_inv_small_data', (0,1), 2, knownfailure='gdtrix bad some points'),
        data(gdtrix_comp, 'gamma_inv_data_ipp-gamma_inv_data', (0,1), 3, rtol=6e-15),
        data(gdtrix_comp, 'gamma_inv_big_data_ipp-gamma_inv_big_data', (0,1), 3),

        data(chndtr, 'nccs_ipp-nccs', (2,0,1), 3, rtol=3e-5),
        data(chndtr, 'nccs_big_ipp-nccs_big', (2,0,1), 3, rtol=5e-4, knownfailure='chndtr inaccurate some points'),

        data(sph_harm_, 'spherical_harmonic_ipp-spherical_harmonic', (1,0,3,2), (4,5), rtol=5e-11,
             param_filter=(lambda p: np.ones(p.shape, '?'),
                           lambda p: np.ones(p.shape, '?'),
                           lambda p: np.logical_and(p < 2*np.pi, p >= 0),
                           lambda p: np.logical_and(p < np.pi, p >= 0))),

        data(spherical_jn_, 'sph_bessel_data_ipp-sph_bessel_data', (0,1), 2, rtol=1e-13),
        data(spherical_yn_, 'sph_neumann_data_ipp-sph_neumann_data', (0,1), 2, rtol=8e-15),

        # -- not used yet (function does not exist in scipy):
        # 'ellint_pi2_data_ipp-ellint_pi2_data',
        # 'ellint_pi3_data_ipp-ellint_pi3_data',
        # 'ellint_pi3_large_data_ipp-ellint_pi3_large_data',
        # 'ellint_rc_data_ipp-ellint_rc_data',
        # 'ellint_rd_data_ipp-ellint_rd_data',
        # 'ellint_rf_data_ipp-ellint_rf_data',
        # 'ellint_rj_data_ipp-ellint_rj_data',
        # 'ncbeta_big_ipp-ncbeta_big',
        # 'ncbeta_ipp-ncbeta',
        # 'powm1_sqrtp1m1_test_cpp-powm1_data',
        # 'powm1_sqrtp1m1_test_cpp-sqrtp1m1_data',
        # 'test_gamma_data_ipp-gammap1m1_data',
        # 'tgamma_ratio_data_ipp-tgamma_ratio_data',
    ]

    for test in TESTS:
        yield _test_factory, test
