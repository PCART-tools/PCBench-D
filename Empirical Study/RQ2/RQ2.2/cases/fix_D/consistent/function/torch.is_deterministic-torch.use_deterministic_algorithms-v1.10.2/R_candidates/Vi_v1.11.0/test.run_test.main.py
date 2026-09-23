def main():
    options = parse_args()

    # TODO: move this export & download function in tools/ folder
    test_times_filename = options.export_past_test_times
    if test_times_filename:
        print(
            f"Exporting past test times from S3 to {test_times_filename}, no tests will be run."
        )
        export_S3_test_times(test_times_filename)
        return

    specified_test_cases_filename = options.run_specified_test_cases
    if specified_test_cases_filename:
        print(
            f"Loading specified test cases to run from {specified_test_cases_filename}."
        )
        global SPECIFIED_TEST_CASES_DICT
        SPECIFIED_TEST_CASES_DICT = get_specified_test_cases(
            specified_test_cases_filename, TESTS
        )

    test_directory = str(REPO_ROOT / "test")
    selected_tests = get_selected_tests(options)

    if options.verbose:
        print_to_stderr("Selected tests: {}".format(", ".join(selected_tests)))

    if options.coverage and not PYTORCH_COLLECT_COVERAGE:
        shell(["coverage", "erase"])

    # NS: Disable target determination until it can be made more reliable
    # if options.determine_from is not None and os.path.exists(options.determine_from):
    #     slow_tests = get_slow_tests_based_on_S3(
    #         TESTS, TARGET_DET_LIST, SLOW_TEST_THRESHOLD
    #     )
    #     print_to_stderr(
    #         "Added the following tests to target_det tests as calculated based on S3:"
    #     )
    #     print_to_stderr(slow_tests)
    #     with open(options.determine_from, "r") as fh:
    #         touched_files = [
    #             os.path.normpath(name.strip())
    #             for name in fh.read().split("\n")
    #             if len(name.strip()) > 0
    #         ]
    #     # HACK: Ensure the 'test' paths can be traversed by Modulefinder
    #     sys.path.append(test_directory)
    #     selected_tests = [
    #         test
    #         for test in selected_tests
    #         if should_run_test(
    #             TARGET_DET_LIST + slow_tests, test, touched_files, options
    #         )
    #     ]
    #     sys.path.remove(test_directory)

    if IS_IN_CI:
        selected_tests = get_reordered_tests(
            selected_tests, ENABLE_PR_HISTORY_REORDERING
        )
        # downloading test cases configuration to local environment
        get_test_case_configs(dirpath=test_directory)

    has_failed = False
    failure_messages = []
    try:
        for test in selected_tests:
            options_clone = copy.deepcopy(options)
            if test in USE_PYTEST_LIST:
                options_clone.pytest = True
            err_message = run_test_module(test, test_directory, options_clone)
            if err_message is None:
                continue
            has_failed = True
            failure_messages.append(err_message)
            if not options_clone.continue_through_error:
                raise RuntimeError(err_message)
            print_to_stderr(err_message)
    finally:
        if options.coverage:
            from coverage import Coverage

            with set_cwd(test_directory):
                cov = Coverage()
                if PYTORCH_COLLECT_COVERAGE:
                    cov.load()
                cov.combine(strict=False)
                cov.save()
                if not PYTORCH_COLLECT_COVERAGE:
                    cov.html_report()

    if options.continue_through_error and has_failed:
        for err in failure_messages:
            print_to_stderr(err)
        sys.exit(1)
