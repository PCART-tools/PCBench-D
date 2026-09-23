def export_slow_tests(options: Any) -> None:
    filename = options.filename
    if os.path.exists(filename):
        print(f'Overwriting existent file: {filename}')
    with open(filename, 'w+') as file:
        slow_test_times: Dict[str, float] = filter_slow_tests(get_test_case_times())
        if options.ignore_small_diffs:
            test_infra_slow_tests_dict = get_test_infra_slow_tests()
            if too_similar(slow_test_times, test_infra_slow_tests_dict, options.ignore_small_diffs):
                slow_test_times = test_infra_slow_tests_dict
        json.dump(slow_test_times, file, indent='    ', separators=(',', ': '), sort_keys=True)
        file.write('\n')
