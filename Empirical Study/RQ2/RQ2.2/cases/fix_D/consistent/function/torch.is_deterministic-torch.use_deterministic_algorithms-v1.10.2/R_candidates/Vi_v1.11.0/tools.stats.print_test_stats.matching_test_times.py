def matching_test_times(
    *,
    base_reports: Dict[Commit, List[SimplerReport]],
    filename: str,
    suite_name: str,
    case_name: str,
    status: Status,
) -> List[float]:
    times: List[float] = []
    for reports in base_reports.values():
        for report in reports:
            file_data = report.get(filename)
            if file_data:
                suite = file_data.get(suite_name)
                if suite:
                    case = suite.get(case_name)
                    if case:
                        t = case['seconds']
                        s = case['status']
                        if s == status:
                            times.append(t)
    return times
