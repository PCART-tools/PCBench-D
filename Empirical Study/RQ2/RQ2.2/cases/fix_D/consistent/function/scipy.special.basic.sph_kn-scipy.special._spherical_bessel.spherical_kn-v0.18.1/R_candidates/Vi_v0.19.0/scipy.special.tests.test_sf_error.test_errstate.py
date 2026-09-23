def test_errstate():
    for category in _sf_error_code_map.keys():
        for action in _sf_error_actions:
            olderr = sc.geterr()
            with sc.errstate(**{category: action}):
                _check_action(_sf_error_test_function,
                              (_sf_error_code_map[category],),
                              action)
            assert_equal(olderr, sc.geterr())
