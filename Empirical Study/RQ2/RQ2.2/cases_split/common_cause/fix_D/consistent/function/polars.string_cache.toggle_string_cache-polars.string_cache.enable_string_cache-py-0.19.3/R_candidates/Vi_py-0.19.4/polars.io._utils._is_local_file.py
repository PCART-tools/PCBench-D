def _is_local_file(file: str) -> bool:
    try:
        next(glob.iglob(file, recursive=True))  # noqa: PTH207
    except StopIteration:
        return False
    else:
        return True
