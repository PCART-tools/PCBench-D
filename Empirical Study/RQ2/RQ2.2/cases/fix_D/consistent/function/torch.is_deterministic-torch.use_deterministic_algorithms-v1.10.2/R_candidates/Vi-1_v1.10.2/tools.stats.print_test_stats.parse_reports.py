def parse_reports(folder: str) -> Dict[str, TestFile]:
    tests_by_file = dict()
    for report in get_recursive_files(folder, ".xml"):
        report_path = Path(report)
        # basename of the directory of test-report is the test filename
        test_filename = re.sub(r'\.', '/', report_path.parent.name)
        # test type is the parent directory (only applies to dist-*)
        # See: CUSTOM_HANDLERS in test/run_test.py
        test_type = report_path.parent.parent.name
        if test_filename not in tests_by_file:
            tests_by_file[test_filename] = TestFile(test_filename)
        for test_case in parse_report(report):
            tests_by_file[test_filename].append(test_case, test_type)
    return tests_by_file
