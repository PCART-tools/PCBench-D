def load_tests(loader, tests, pattern):
    set_running_script_path()
    test_suite = unittest.TestSuite()
    for test_group in tests:
        for test in test_group:
            check_test_defined_in_running_script(test)
            test_suite.addTest(test)
    return test_suite
