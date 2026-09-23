def get_test_case_times() -> Dict[str, float]:
    reports: List[Report] = get_previous_reports_for_branch('origin/viable/strict', "")
    # an entry will be like ("test_doc_examples (__main__.TestTypeHints)" -> [values]))
    test_names_to_times: DefaultDict[str, List[float]] = defaultdict(list)
    for report in reports:
        if report.get('format_version', 1) != 2:  # type: ignore[misc]
            raise RuntimeError("S3 format currently handled is version 2 only")
        v2report = cast(Version2Report, report)
        for test_file in v2report['files'].values():
            for suitename, test_suite in test_file['suites'].items():
                for casename, test_case in test_suite['cases'].items():
                    # The below attaches a __main__ as that matches the format of test.__class__ in
                    # common_utils.py (where this data will be used), and also matches what the output
                    # of a running test would look like.
                    name = f'{casename} (__main__.{suitename})'
                    succeeded: bool = test_case['status'] is None
                    if succeeded:
                        test_names_to_times[name].append(test_case['seconds'])
    return {test_case: statistics.mean(times) for test_case, times in test_names_to_times.items()}
