def build_message(
    test_file: TestFile,
    test_suite: TestSuite,
    test_case: TestCase,
    meta_info: ReportMetaMeta
) -> Dict[str, Dict[str, Any]]:
    return {
        "normal": {
            **meta_info,
            "test_filename": test_file.name,
            "test_suite_name": test_suite.name,
            "test_case_name": test_case.name,
        },
        "int": {
            "time": int(time.time()),
            "test_total_count": 1,
            "test_total_time": int(test_case.time * 1000),
            "test_failed_count": 1 if test_case.failed > 0 else 0,
            "test_skipped_count": 1 if test_case.skipped > 0 else 0,
            "test_errored_count": 1 if test_case.errored > 0 else 0,
        },
    }
