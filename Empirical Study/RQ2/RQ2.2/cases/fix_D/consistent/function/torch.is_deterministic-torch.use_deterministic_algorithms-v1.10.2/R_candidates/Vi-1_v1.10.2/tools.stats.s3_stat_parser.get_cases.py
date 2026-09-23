def get_cases(
    *,
    data: Report,
    filename: Optional[str],
    suite_name: Optional[str],
    test_name: Optional[str],
) -> List[Version2Case]:
    cases: List[Version2Case] = []
    if 'format_version' not in data:  # version 1 implicitly
        v1report = cast(Version1Report, data)
        suites = v1report['suites']
        for sname, v1suite in suites.items():
            if not suite_name or sname == suite_name:
                for v1case in v1suite['cases']:
                    if not test_name or v1case['name'] == test_name:
                        cases.append(newify_case(v1case))
    else:
        v_report = cast(VersionedReport, data)
        version = v_report['format_version']
        if version == 2:
            v2report = cast(Version2Report, v_report)
            for fname, v2file in v2report['files'].items():
                if fname == filename or not filename:
                    for sname, v2suite in v2file['suites'].items():
                        if sname == suite_name or not suite_name:
                            for cname, v2case in v2suite['cases'].items():
                                if not test_name or cname == test_name:
                                    cases.append(v2case)
        else:
            raise RuntimeError(f'Unknown format version: {version}')
    return cases
