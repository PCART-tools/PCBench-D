def _strip_filename(msg: str) -> str:
    """Strip the filename from a mypy message."""
    _, tail = os.path.splitdrive(msg)
    return tail.split(":", 1)[-1]
