def check_if_enable(test: unittest.TestCase):
    test_suite = str(test.__class__).split('\'')[1]
    test_name = f'{test._testMethodName} ({test_suite})'
    if slow_tests_dict is not None and test_name in slow_tests_dict:
        getattr(test, test._testMethodName).__dict__['slow_test'] = True
        if not TEST_WITH_SLOW:
            raise unittest.SkipTest("test is slow; run with PYTORCH_TEST_WITH_SLOW to enable test")
    if not IS_SANDCASTLE and disabled_tests_dict is not None:
        if test_name in disabled_tests_dict:
            issue_url, platforms = disabled_tests_dict[test_name]
            platform_to_conditional: Dict = {
                "mac": IS_MACOS,
                "macos": IS_MACOS,
                "win": IS_WINDOWS,
                "windows": IS_WINDOWS,
                "linux": IS_LINUX,
                "rocm": TEST_WITH_ROCM
            }
            if platforms == [] or any([platform_to_conditional[platform] for platform in platforms]):
                raise unittest.SkipTest(
                    f"Test is disabled because an issue exists disabling it: {issue_url}" +
                    f" for {'all' if platforms == [] else ''}platform(s) {', '.join(platforms)}. " +
                    "If you're seeing this on your local machine and would like to enable this test, " +
                    "please make sure IN_CI is not set and you are not using the flag --import-disabled-tests.")
    if TEST_SKIP_FAST:
        if not getattr(test, test._testMethodName).__dict__.get('slow_test', False):
            raise unittest.SkipTest("test is fast; we disabled it with PYTORCH_TEST_SKIP_FAST")
