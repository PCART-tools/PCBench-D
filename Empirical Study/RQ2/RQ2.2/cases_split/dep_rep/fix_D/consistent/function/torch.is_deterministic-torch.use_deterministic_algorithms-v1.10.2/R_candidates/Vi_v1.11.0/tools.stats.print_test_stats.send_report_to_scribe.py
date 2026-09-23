def send_report_to_scribe(reports: Dict[str, TestFile]) -> None:
    meta_info = build_info()
    logs = json.dumps(
        [
            {
                "category": "perfpipe_pytorch_test_times",
                "message": json.dumps(build_message(test_file, test_suite, test_case, meta_info)),
                "line_escape": False,
            }
            for test_file in reports.values()
            for test_suite in test_file.test_suites.values()
            for test_case in test_suite.test_cases.values()
        ]
    )
    # no need to print send result as exceptions will be captured and print later.
    send_to_scribe(logs)
