def make_lines(
    *,
    jobs: Set[str],
    jsons: Dict[str, List[Report]],
    filename: Optional[str],
    suite_name: Optional[str],
    test_name: str,
) -> List[str]:
    lines = []
    for job, reports in jsons.items():
        for data in reports:
            cases = get_cases(
                data=data,
                filename=filename,
                suite_name=suite_name,
                test_name=test_name,
            )
            if cases:
                case = cases[0]
                status = case['status']
                line = f'{job} {case["seconds"]}s{f" {status}" if status else ""}'
                if len(cases) > 1:
                    line += f' ({len(cases) - 1} matching suites omitted)'
                lines.append(line)
            elif job in jobs:
                lines.append(f'{job} (test not found)')
    if lines:
        return lines
    else:
        return ['(no reports in S3)']
