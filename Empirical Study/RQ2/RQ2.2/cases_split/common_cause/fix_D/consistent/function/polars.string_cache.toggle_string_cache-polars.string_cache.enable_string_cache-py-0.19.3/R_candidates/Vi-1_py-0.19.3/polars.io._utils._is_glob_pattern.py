def _is_glob_pattern(file: str) -> bool:
    return any(char in file for char in ["*", "?", "["])
