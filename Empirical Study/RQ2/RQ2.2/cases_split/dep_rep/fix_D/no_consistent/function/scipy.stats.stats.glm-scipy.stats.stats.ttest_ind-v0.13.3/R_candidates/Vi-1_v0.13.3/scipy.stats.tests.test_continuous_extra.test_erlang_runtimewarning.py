def test_erlang_runtimewarning():
    # erlang should generate a RuntimeWarning if a non-integer
    # shape parameter is used.
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)

        # The non-integer shape parameter 1.3 should trigger a RuntimeWarning
        npt.assert_raises(RuntimeWarning,
                          stats.erlang.rvs, 1.3, loc=0, scale=1, size=4)

        # Calling the fit method with `f0` set to an integer should
        # *not* trigger a RuntimeWarning.  It should return the same
        # values as gamma.fit(...).
        data = [0.5, 1.0, 2.0, 4.0]
        result_erlang = stats.erlang.fit(data, f0=1)
        result_gamma = stats.gamma.fit(data, f0=1)
        npt.assert_allclose(result_erlang, result_gamma, rtol=1e-3)
