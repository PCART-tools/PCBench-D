def case_delta(case: CaseDiff) -> Stat:
    was = case['was']
    now = case['now']
    return recenter(
        was[0] if was else zero_stat(),
        now['seconds'] if now else 0,
    )
