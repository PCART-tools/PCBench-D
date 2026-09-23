def run_tests(argv=UNITTEST_ARGS):
    # import test files.
    if IMPORT_SLOW_TESTS:
        if os.path.exists(IMPORT_SLOW_TESTS):
            global slow_tests_dict
            with open(IMPORT_SLOW_TESTS, 'r') as fp:
                slow_tests_dict = json.load(fp)
        else:
            print(f'[WARNING] slow test file provided but not found: {IMPORT_SLOW_TESTS}')
    if IMPORT_DISABLED_TESTS:
        if os.path.exists(IMPORT_DISABLED_TESTS):
            global disabled_tests_dict
            with open(IMPORT_DISABLED_TESTS, 'r') as fp:
                disabled_tests_dict = json.load(fp)
        else:
            print(f'[WARNING] disabled test file provided but not found: {IMPORT_DISABLED_TESTS}')
    # Determine the test launch mechanism
    if TEST_DISCOVER:
        _print_test_names()
    elif TEST_IN_SUBPROCESS:
        suite = unittest.TestLoader().loadTestsFromModule(__main__)
        test_cases = discover_test_cases_recursively(suite)
        failed_tests = []
        for case in test_cases:
            test_case_full_name = case.id().split('.', 1)[1]
            exitcode = shell([sys.executable] + argv + [test_case_full_name])
            if exitcode != 0:
                failed_tests.append(test_case_full_name)

        assert len(failed_tests) == 0, "{} unit test(s) failed:\n\t{}".format(
            len(failed_tests), '\n\t'.join(failed_tests))
    elif RUN_PARALLEL > 1:
        suite = unittest.TestLoader().loadTestsFromModule(__main__)
        test_cases = discover_test_cases_recursively(suite)
        test_batches = chunk_list(get_test_names(test_cases), RUN_PARALLEL)
        processes = []
        for i in range(RUN_PARALLEL):
            command = [sys.executable] + argv + ['--log-suffix=-shard-{}'.format(i + 1)] + test_batches[i]
            processes.append(subprocess.Popen(command, universal_newlines=True))
        failed = False
        for p in processes:
            failed |= wait_for_process(p) != 0
        assert not failed, "Some test shards have failed"
    elif TEST_SAVE_XML is not None:
        # import here so that non-CI doesn't need xmlrunner installed
        import xmlrunner  # type: ignore[import]
        test_filename = sanitize_test_filename(inspect.getfile(sys._getframe(1)))
        test_report_path = TEST_SAVE_XML + LOG_SUFFIX
        test_report_path = os.path.join(test_report_path, test_filename)
        os.makedirs(test_report_path, exist_ok=True)
        verbose = '--verbose' in argv or '-v' in argv
        if verbose:
            print('Test results will be stored in {}'.format(test_report_path))
        unittest.main(argv=argv, testRunner=xmlrunner.XMLTestRunner(output=test_report_path, verbosity=2 if verbose else 1))
    elif REPEAT_COUNT > 1:
        for _ in range(REPEAT_COUNT):
            if not unittest.main(exit=False, argv=argv).result.wasSuccessful():
                sys.exit(-1)
    else:
        unittest.main(argv=argv)
