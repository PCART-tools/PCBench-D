def anomalies(diffs: List[SuiteDiff]) -> str:
    return ''.join(map(display_suite_diff, diffs))
