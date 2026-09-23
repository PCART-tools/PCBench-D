def assert_fp_equal(x, y, err_msg="", nulp=50):
    """Assert two arrays are equal, up to some floating-point rounding error"""
    try:
        assert_array_almost_equal_nulp(x, y, nulp)
    except AssertionError as e:
        raise AssertionError("%s\n%s" % (e, err_msg))
