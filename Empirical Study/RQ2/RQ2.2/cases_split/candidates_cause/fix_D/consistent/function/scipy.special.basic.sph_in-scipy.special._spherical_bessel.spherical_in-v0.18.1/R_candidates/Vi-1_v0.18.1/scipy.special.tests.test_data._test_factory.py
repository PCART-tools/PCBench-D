def _test_factory(test, dtype=np.double):
    """Boost test"""
    olderr = np.seterr(all='ignore')
    try:
        test.check(dtype=dtype)
    finally:
        np.seterr(**olderr)
