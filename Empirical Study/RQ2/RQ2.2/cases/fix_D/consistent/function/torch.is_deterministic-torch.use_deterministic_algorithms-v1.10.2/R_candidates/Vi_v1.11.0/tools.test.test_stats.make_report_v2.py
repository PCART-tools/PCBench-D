def make_report_v2(tests: Dict[str, Dict[str, Dict[str, Version2Case]]]) -> Version2Report:
    files = {}
    for file_name, file_suites in tests.items():
        suites = {
            suite_name: {
                'total_seconds': sum(case['seconds'] for case in cases.values()),
                'cases': cases,
            }
            for suite_name, cases in file_suites.items()
        }
        files[file_name] = {
            'suites': suites,
            'total_seconds': sum(suite['total_seconds'] for suite in suites.values()),
        }
    return {
        **dummy_meta_meta(),  # type: ignore[misc]
        'format_version': 2,
        'total_seconds': sum(s['total_seconds'] for s in files.values()),
        'files': files,
    }
