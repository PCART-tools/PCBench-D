def _is_local_file(file: str) -> bool:
    try:
        next(glob.iglob(file, recursive=True))
        return True
    except StopIteration:
        return False
