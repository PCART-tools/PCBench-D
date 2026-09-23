def main() -> None:
    options = parse_args()
    testcases = parse_junit_reports(options.report_path)
    render_tests(testcases)
