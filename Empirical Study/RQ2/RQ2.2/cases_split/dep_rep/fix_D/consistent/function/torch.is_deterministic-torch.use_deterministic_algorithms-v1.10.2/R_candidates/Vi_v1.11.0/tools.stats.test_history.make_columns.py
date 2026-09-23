def make_columns(
    *,
    jobs: List[str],
    jsons: Dict[str, Report],
    omitted: Dict[str, int],
    filename: Optional[str],
    suite_name: Optional[str],
    test_name: str,
    digits: int,
) -> str:
    columns = []
    total_omitted = 0
    total_suites = 0
    for job in jobs:
        data = jsons.get(job)
        column, omitted_suites = make_column(
            data=data,
            filename=filename,
            suite_name=suite_name,
            test_name=test_name,
            digits=digits,
        )
        columns.append(column)
        total_suites += omitted_suites
        if job in omitted:
            total_omitted += omitted[job]
    if total_omitted > 0:
        columns.append(f'({total_omitted} job re-runs omitted)')
    if total_suites > 0:
        columns.append(f'({total_suites} matching suites omitted)')
    return ' '.join(columns)
