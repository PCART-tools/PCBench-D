def assert_tol_equal(a, b, rtol=1e-7, atol=0, err_msg='', verbose=True):
    """Assert that `a` and `b` are equal to tolerance ``atol + rtol*abs(b)``"""
    def compare(x, y):
        return np.allclose(x, y, rtol=rtol, atol=atol)
    a, b = np.asanyarray(a), np.asanyarray(b)
    header = 'Not equal to tolerance rtol=%g, atol=%g' % (rtol, atol)
    np.testing.utils.assert_array_compare(compare, a, b, err_msg=str(err_msg),
                                          verbose=verbose, header=header)
