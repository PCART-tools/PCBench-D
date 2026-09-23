def summary_line(message: str, d: DefaultDict[str, List[CaseDiff]]) -> str:
    all_cases = [c for cs in d.values() for c in cs]
    tests = len(all_cases)
    suites = len(d)
    sp = f'{plural(suites)})'.ljust(2)
    tp = f'{plural(tests)},'.ljust(2)
    # there might be a bug calculating this stdev, not sure
    stat = sum_normals(case_delta(c) for c in all_cases)
    return ''.join([
        f'{message} (across {suites:>4} suite{sp}',
        f'{tests:>6} test{tp}',
        f' totaling {display_final_stat(stat)}',
    ])
