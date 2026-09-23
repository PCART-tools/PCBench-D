def _assert_success(res, desired_fun=None, desired_x=None,
                    rtol=1e-8, atol=1e-8):
    # res: linprog result object
    # desired_fun: desired objective function value or None
    # desired_x: desired solution or None
    if not res.success:
        msg = "linprog status {0}, message: {1}".format(res.status,
                                                        res.message)
        raise AssertionError(msg)

    assert_equal(res.status, 0)
    if desired_fun is not None:
        assert_allclose(res.fun, desired_fun,
                        err_msg="converged to an unexpected objective value",
                        rtol=rtol, atol=atol)
    if desired_x is not None:
        assert_allclose(res.x, desired_x,
                        err_msg="converged to an unexpected solution",
                        rtol=rtol, atol=atol)
