@dec.slow
@check_version(mp, '0.19')
@check_version(sympy, '0.7')
@dec.knownfailureif(_is_32bit_platform, "rtol only 2e-11, see gh-6938")
def test_alpha():
    # Test data for the alpha_k. See DLMF 8.12.14.
    with mp.workdps(30):
        alpha = [mp.mpf(0), mp.mpf(1), mp.mpf(1)/3, mp.mpf(1)/36,
                 -mp.mpf(1)/270, mp.mpf(1)/4320, mp.mpf(1)/17010,
                 -mp.mpf(139)/5443200, mp.mpf(1)/204120]
        mp_assert_allclose(compute_alpha(9), alpha)
