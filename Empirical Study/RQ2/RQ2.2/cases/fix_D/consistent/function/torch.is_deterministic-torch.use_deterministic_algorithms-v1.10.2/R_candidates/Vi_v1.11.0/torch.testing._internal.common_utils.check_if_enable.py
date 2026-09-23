def check_if_enable(test: unittest.TestCase):
    test_suite = str(test.__class__).split('\'')[1]
    raw_test_name = f'{test._testMethodName} ({test_suite})'
    if slow_tests_dict is not None and raw_test_name in slow_tests_dict:
        getattr(test, test._testMethodName).__dict__['slow_test'] = True
        if not TEST_WITH_SLOW:
            raise unittest.SkipTest("test is slow; run with PYTORCH_TEST_WITH_SLOW to enable test")
    sanitized_test_method_name = remove_device_and_dtype_suffixes(test._testMethodName)
    if not IS_SANDCASTLE and disabled_tests_dict is not None:
        for disabled_test, (issue_url, platforms) in disabled_tests_dict.items():
            disable_test_parts = disabled_test.split()
            if len(disable_test_parts) > 1:
                disabled_test_name = disable_test_parts[0]
                disabled_test_suite = disable_test_parts[1][1:-1]
                # if test method name or its sanitized version exactly matches the disabled test method name
                # AND allow non-parametrized suite names to disable parametrized ones (TestSuite disables TestSuiteCPU)
                if (test._testMethodName == disabled_test_name or sanitized_test_method_name == disabled_test_name) \
                   and disabled_test_suite in test_suite:
                    platform_to_conditional: Dict = {
                        "mac": IS_MACOS,
                        "macos": IS_MACOS,
                        "win": IS_WINDOWS,
                        "windows": IS_WINDOWS,
                        "linux": IS_LINUX,
                        "rocm": TEST_WITH_ROCM,
                        "asan": TEST_WITH_ASAN
                    }
                    if platforms == [] or any([platform_to_conditional[platform] for platform in platforms]):
                        skip_msg = f"Test is disabled because an issue exists disabling it: {issue_url}" \
                            f" for {'all' if platforms == [] else ''}platform(s) {', '.join(platforms)}. " \
                            "If you're seeing this on your local machine and would like to enable this test, " \
                            "please make sure IN_CI is not set and you are not using the flag --import-disabled-tests."
                        raise unittest.SkipTest(skip_msg)
    if TEST_SKIP_FAST:
        if not getattr(test, test._testMethodName).__dict__.get('slow_test', False):
            raise unittest.SkipTest("test is fast; we disabled it with PYTORCH_TEST_SKIP_FAST")
