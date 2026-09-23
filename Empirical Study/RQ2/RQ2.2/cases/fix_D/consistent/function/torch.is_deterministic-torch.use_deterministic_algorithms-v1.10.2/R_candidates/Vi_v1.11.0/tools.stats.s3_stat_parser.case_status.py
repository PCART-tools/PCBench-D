def case_status(case: Version1Case) -> Status:
    for k in {'errored', 'failed', 'skipped'}:
        if case[k]:  # type: ignore[misc]
            return cast(Status, k)
    return None
