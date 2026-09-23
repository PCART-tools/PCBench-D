def caffe2_flaky(test_method):
    # This decorator is used to mark a test method as flaky.
    # This is used in conjunction with the environment variable
    # CAFFE2_RUN_FLAKY_TESTS that specifies "flaky tests" mode
    # If flaky tests mode are on, only flaky tests are run
    # If flaky tests mode are off, only non-flaky tests are run
    # NOTE: the decorator should be applied as the top-level decorator
    # in a test method.
    test_method.__caffe2_flaky__ = True
    return test_method
