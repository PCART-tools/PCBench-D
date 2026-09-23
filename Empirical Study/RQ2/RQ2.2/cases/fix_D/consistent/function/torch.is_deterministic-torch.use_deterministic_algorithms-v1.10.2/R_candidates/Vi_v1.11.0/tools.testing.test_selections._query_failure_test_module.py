def _query_failure_test_module(reports: List[Tuple["Report", str]]) -> List[str]:
    test_modules: List[str] = []
    if len(reports) == 0 or len(reports[0]) == 0:
        return test_modules
    report = reports[0][0]
    v_report = cast(Version2Report, report)
    assert 'format_version' in v_report.keys() and v_report.get('format_version') == 2, \
        "S3 format currently handled is version 2 only"
    files: Dict[str, Any] = v_report['files']
    for fname, file in files.items():
        contains_failure = any(
            any(case['status'] == 'errored' or case['status'] == 'failed'
                for _, case in suite['cases'].items())
            for _, suite in file['suites'].items())
        if contains_failure:
            test_modules.append(fname)
    return test_modules
