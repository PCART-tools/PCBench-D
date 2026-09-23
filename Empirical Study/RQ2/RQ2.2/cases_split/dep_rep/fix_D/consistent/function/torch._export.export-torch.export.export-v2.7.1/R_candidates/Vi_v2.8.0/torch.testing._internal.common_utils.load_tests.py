def load_tests(loader, tests, pattern):
    set_running_script_path()
    test_suite = unittest.TestSuite()
    for test_group in tests:
        if not DISABLE_RUNNING_SCRIPT_CHK:
            for test in test_group:
                check_test_defined_in_running_script(test)
        if test_group._tests:
            test_suite.addTest(test_group)
    return test_suite
