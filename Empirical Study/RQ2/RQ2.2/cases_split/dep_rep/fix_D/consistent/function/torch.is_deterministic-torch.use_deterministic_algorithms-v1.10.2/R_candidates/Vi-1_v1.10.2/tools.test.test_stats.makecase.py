def makecase(
    name: str,
    seconds: float,
    *,
    errored: bool = False,
    failed: bool = False,
    skipped: bool = False,
) -> Version1Case:
    return {
        'name': name,
        'seconds': seconds,
        'errored': errored,
        'failed': failed,
        'skipped': skipped,
    }
