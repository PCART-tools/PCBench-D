def test_seterr():
    entry_err = sc.geterr()
    try:
        for category in _sf_error_code_map.keys():
            for action in _sf_error_actions:
                geterr_olderr = sc.geterr()
                seterr_olderr = sc.seterr(**{category: action})
                assert_(geterr_olderr == seterr_olderr)
                newerr = sc.geterr()
                assert_(newerr[category] == action)
                geterr_olderr.pop(category)
                newerr.pop(category)
                assert_(geterr_olderr == newerr)
                _check_action(_sf_error_test_function,
                              (_sf_error_code_map[category],),
                               action)
    finally:
        sc.seterr(**entry_err)
