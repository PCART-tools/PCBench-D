def reports_has_no_tests(reports: Dict[str, TestFile]) -> bool:
    for test_file in reports.values():
        for test_suite in test_file.test_suites.values():
            if len(test_suite.test_cases) > 0:
                return False
    return True
