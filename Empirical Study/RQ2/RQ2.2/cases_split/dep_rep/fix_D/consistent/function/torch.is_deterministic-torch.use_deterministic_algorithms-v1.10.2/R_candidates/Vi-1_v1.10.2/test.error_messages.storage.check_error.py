def check_error(desc, fn, *required_substrings):
    try:
        fn()
    except Exception as e:
        error_message = e.args[0]
        print('=' * 80)
        print(desc)
        print('-' * 80)
        print(error_message)
        print('')
        for sub in required_substrings:
            assert sub in error_message
        return
    raise AssertionError("given function ({}) didn't raise an error".format(desc))
