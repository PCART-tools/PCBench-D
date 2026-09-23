def make_report_v1(tests: Dict[str, List[Version1Case]]) -> Version1Report:
    suites = {
        suite_name: {
            'total_seconds': sum(case['seconds'] for case in cases),
            'cases': cases,
        }
        for suite_name, cases in tests.items()
    }
    return {
        **dummy_meta_meta(),  # type: ignore[misc]
        'total_seconds': sum(s['total_seconds'] for s in suites.values()),
        'suites': suites,
    }
