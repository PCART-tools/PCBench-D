def process_intentional_test_runs(runs: List[TestCase]) -> Tuple[int, int]:
    num_fail = 0
    num_expected_fail = 0
    num_pass = 0
    num_unexpected_success = 0
    num_errored = 0
    num_skipped = 0
    for test_run in runs:
        if test_run.failed:
            num_fail += 1
        elif test_run.expected_failure:
            num_expected_fail += 1
        elif test_run.unexpected_success:
            num_unexpected_success += 1
        elif test_run.errored:
            num_errored += 1
        elif test_run.skipped:
            num_skipped += 1
        else:
            num_pass += 1

    REPEAT_TEST_FOR_TYPES_TESTS = [
        "test_data_parallel_module",
        "test_data_parallel_module_kwargs_only",
        "test_data_parallel_module_kwargs_only_empty_list",
        "test_data_parallel_module_kwargs_only_empty_dict",
        "test_data_parallel_module_kwargs_only_empty_tuple"
    ]

    # Do not run checks for tests that use repeat_test_for_types decorator as they do not go well with our retry
    # functionality. Once issue https://github.com/pytorch/pytorch/issues/69865 is fixed, we should remove the exception
    if not any([x in test_run.name for x in REPEAT_TEST_FOR_TYPES_TESTS]):
        err_msg = f'Warning: unintentional test case duplicates found for {test_run.name} in suite {test_run.class_name}.'
        report_only = os.getenv('PYTORCH_OVERRIDE_FLAKY_SIGNAL') != '1'
        if report_only and num_fail + num_errored + num_unexpected_success < 1 or not report_only and num_expected_fail < 1:
            raise RuntimeWarning(f'{err_msg} Intentional reruns are only triggered when the first run fails or errors, but'
                                 ' we found no failures nor errors.')
        if num_unexpected_success + num_expected_fail < 1:
            raise RuntimeWarning(f'{err_msg} Intentional reruns should raise at least one unexpected success or expected '
                                 'failure, but none have been found.')
        if report_only and num_pass != num_unexpected_success:
            raise RuntimeWarning(f'{err_msg} Every success in an intentional rerun is shadowed by one unexpected success.'
                                 f'However, successes = {num_pass} and unexpected successes = {num_unexpected_success}')
        if not report_only and num_pass > 1:
            raise RuntimeWarning(f'{err_msg} There should be at most 1 successful run in an intentional rerun that stops'
                                 f' at first success. The number of successful runs = {num_pass}')
        if num_skipped > 0:
            raise RuntimeWarning(f'{err_msg} No skips should occur in intentional reruns, but skips = {num_skipped}')
    return max(num_unexpected_success, num_pass), num_fail + num_expected_fail + num_errored
