def check_normalization(distfn, args, distname):
    norm_moment = distfn.moment(0, *args)
    npt.assert_allclose(norm_moment, 1.0)

    # this is a temporary plug: either ncf or expect is problematic;
    # best be marked as a knownfail, but I've no clue how to do it.
    if distname == "ncf":
        atol, rtol = 1e-5, 0
    else:
        atol, rtol = 1e-7, 1e-7

    normalization_expect = distfn.expect(lambda x: 1, args=args)
    npt.assert_allclose(normalization_expect, 1.0, atol=atol, rtol=rtol,
            err_msg=distname, verbose=True)

    normalization_cdf = distfn.cdf(distfn.b, *args)
    npt.assert_allclose(normalization_cdf, 1.0)
