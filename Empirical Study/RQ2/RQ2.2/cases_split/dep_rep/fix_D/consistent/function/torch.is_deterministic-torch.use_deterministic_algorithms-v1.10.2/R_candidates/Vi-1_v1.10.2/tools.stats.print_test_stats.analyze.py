def analyze(
    *,
    head_report: SimplerReport,
    base_reports: Dict[Commit, List[SimplerReport]],
) -> List[SuiteDiff]:
    nonempty_shas = [sha for sha, reports in base_reports.items() if reports]
    # most recent master ancestor with at least one S3 report,
    # or empty list if there are none (will show all tests as added)
    base_report = base_reports[nonempty_shas[0]] if nonempty_shas else []

    # find all relevant suites (those in either base or head or both)
    all_reports = [head_report] + base_report
    all_suites: Set[Tuple[str, str]] = {
        (filename, suite_name)
        for r in all_reports
        for filename, file_data in r.items()
        for suite_name in file_data.keys()
    }

    removed_suites: List[SuiteDiff] = []
    modified_suites: List[SuiteDiff] = []
    added_suites: List[SuiteDiff] = []

    for filename, suite_name in sorted(all_suites):
        case_diffs: List[CaseDiff] = []
        head_suite = head_report.get(filename, {}).get(suite_name)
        base_cases: Dict[str, Status] = dict(sorted(set.intersection(*[
            {
                (n, case['status'])
                for n, case
                in report.get(filename, {}).get(suite_name, {}).items()
            }
            for report in base_report
        ] or [set()])))
        case_stats: Dict[str, Stat] = {}
        if head_suite:
            now = sum(case['seconds'] for case in head_suite.values())
            if any(
                filename in report and suite_name in report[filename]
                for report in base_report
            ):
                removed_cases: List[CaseDiff] = []
                for case_name, case_status in base_cases.items():
                    case_stats[case_name] = list_stat(matching_test_times(
                        base_reports=base_reports,
                        filename=filename,
                        suite_name=suite_name,
                        case_name=case_name,
                        status=case_status,
                    ))
                    if case_name not in head_suite:
                        removed_cases.append({
                            'margin': '-',
                            'name': case_name,
                            'was': (case_stats[case_name], case_status),
                            'now': None,
                        })
                modified_cases: List[CaseDiff] = []
                added_cases: List[CaseDiff] = []
                for head_case_name in sorted(head_suite):
                    head_case = head_suite[head_case_name]
                    if head_case_name in base_cases:
                        stat = case_stats[head_case_name]
                        base_status = base_cases[head_case_name]
                        if head_case['status'] != base_status:
                            modified_cases.append({
                                'margin': '!',
                                'name': head_case_name,
                                'was': (stat, base_status),
                                'now': head_case,
                            })
                    else:
                        added_cases.append({
                            'margin': '+',
                            'name': head_case_name,
                            'was': None,
                            'now': head_case,
                        })
                # there might be a bug calculating this stdev, not sure
                was = sum_normals(case_stats.values())
                case_diffs = removed_cases + modified_cases + added_cases
                if case_diffs:
                    modified_suites.append({
                        'margin': ' ',
                        'name': suite_name,
                        'was': was,
                        'now': now,
                        'cases': case_diffs,
                    })
            else:
                for head_case_name in sorted(head_suite):
                    head_case = head_suite[head_case_name]
                    case_diffs.append({
                        'margin': ' ',
                        'name': head_case_name,
                        'was': None,
                        'now': head_case,
                    })
                added_suites.append({
                    'margin': '+',
                    'name': suite_name,
                    'was': None,
                    'now': now,
                    'cases': case_diffs,
                })
        else:
            for case_name, case_status in base_cases.items():
                case_stats[case_name] = list_stat(matching_test_times(
                    base_reports=base_reports,
                    filename=filename,
                    suite_name=suite_name,
                    case_name=case_name,
                    status=case_status,
                ))
                case_diffs.append({
                    'margin': ' ',
                    'name': case_name,
                    'was': (case_stats[case_name], case_status),
                    'now': None,
                })
            removed_suites.append({
                'margin': '-',
                'name': suite_name,
                # there might be a bug calculating this stdev, not sure
                'was': sum_normals(case_stats.values()),
                'now': None,
                'cases': case_diffs,
            })

    return removed_suites + modified_suites + added_suites
