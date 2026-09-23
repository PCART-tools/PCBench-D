def _check_action(fun, args, action):
    if action == 'warn':
        with warnings.catch_warnings(record=True) as w:
            fun(*args)
            assert_(w[-1].category is sc.SpecialFunctionWarning)
    elif action == 'raise':
        with assert_raises(sc.SpecialFunctionError):
            fun(*args)
    else:
        # action == 'ignore', make sure there are no warnings/exceptions
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            fun(*args)
