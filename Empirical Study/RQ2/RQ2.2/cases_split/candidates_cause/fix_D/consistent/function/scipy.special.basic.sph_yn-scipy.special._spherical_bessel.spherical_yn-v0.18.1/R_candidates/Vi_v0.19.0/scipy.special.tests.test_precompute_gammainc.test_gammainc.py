@check_version(mp, '0.19')
def test_gammainc():
    # Quick check that the gammainc in
    # special._precompute.gammainc_data agrees with mpmath's
    # gammainc.
    assert_mpmath_equal(gammainc,
                        lambda a, x: mp.gammainc(a, b=x, regularized=True),
                        [Arg(0, 100, inclusive_a=False), Arg(0, 100)],
                        nan_ok=False, rtol=1e-17, n=50, dps=50)
