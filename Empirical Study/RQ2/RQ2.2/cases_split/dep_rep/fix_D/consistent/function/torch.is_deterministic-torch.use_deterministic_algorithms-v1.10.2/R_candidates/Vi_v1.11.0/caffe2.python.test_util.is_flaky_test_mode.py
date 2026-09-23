def is_flaky_test_mode():
    return os.getenv('CAFFE2_RUN_FLAKY_TESTS', '0') == '1'
