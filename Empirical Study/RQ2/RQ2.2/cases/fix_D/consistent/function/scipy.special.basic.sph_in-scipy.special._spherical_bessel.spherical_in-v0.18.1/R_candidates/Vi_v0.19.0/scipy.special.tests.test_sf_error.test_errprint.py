def test_errprint():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        flag = sc.errprint(True)
    try:
        assert_(isinstance(flag, bool))
        with warnings.catch_warnings(record=True) as w:
            sc.loggamma(0)
            assert_(w[-1].category is sc.SpecialFunctionWarning)
    finally:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            sc.errprint(flag)
