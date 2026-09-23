def assemble_s3_object(
    reports: Dict[str, TestFile],
    *,
    total_seconds: float,
) -> Version2Report:
    return {
        **build_info(),  # type: ignore[misc]
        'total_seconds': total_seconds,
        'format_version': 2,
        'files': {
            name: {
                'total_seconds': test_file.total_time,
                'suites': {
                    name: {
                        'total_seconds': suite.total_time,
                        'cases': {
                            name: {
                                'seconds': case.time,
                                'status': 'errored' if case.errored else
                                          'failed' if case.failed else
                                          'skipped' if case.skipped else None
                            }
                            for name, case in suite.test_cases.items()
                        },
                    }
                    for name, suite in test_file.test_suites.items()
                }
            }
            for name, test_file in reports.items()
        }
    }
