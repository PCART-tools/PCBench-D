def mp_assert_allclose(res, std, atol=0, rtol=1e-17):
    """
    Compare lists of mpmath.mpf's or mpmath.mpc's directly so that it
    can be done to higher precision than double.

    """
    try:
        len(res)
    except TypeError:
        res = list(res)

    n = len(std)
    if len(res) != n:
        raise AssertionError("Lengths of inputs not equal.")

    failures = []
    for k in range(n):
        try:
            assert_(mpmath.fabs(res[k] - std[k]) <= atol + rtol*mpmath.fabs(std[k]))
        except AssertionError:
            failures.append(k)

    ndigits = int(abs(np.log10(rtol)))
    msg = [""]
    msg.append("Bad results ({} out of {}) for the following points:"
               .format(len(failures), n))
    for k in failures:
        resrep = mpmath.nstr(res[k], ndigits, min_fixed=0, max_fixed=0)
        stdrep = mpmath.nstr(std[k], ndigits, min_fixed=0, max_fixed=0)
        if std[k] == 0:
            rdiff = "inf"
        else:
            rdiff = mpmath.fabs((res[k] - std[k])/std[k])
            rdiff = mpmath.nstr(rdiff, 3)
        msg.append("{}: {} != {} (rdiff {})".format(k, resrep, stdrep, rdiff))
    if failures:
        assert_(False, "\n".join(msg))
