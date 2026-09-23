def repeat_test_for_types(dtypes):
    def repeat_helper(f):
        @wraps(f)
        def call_helper(self, *args):
            for dtype in dtypes:
                with TestCase.subTest(self, dtype=dtype):
                    f(self, *args, dtype=dtype)

        return call_helper
    return repeat_helper
