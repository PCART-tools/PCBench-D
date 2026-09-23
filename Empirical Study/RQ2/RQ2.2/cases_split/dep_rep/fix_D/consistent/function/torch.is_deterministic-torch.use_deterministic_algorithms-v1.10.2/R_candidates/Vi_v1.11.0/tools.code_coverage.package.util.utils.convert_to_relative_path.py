def convert_to_relative_path(whole_path: str, base_path: str) -> str:
    # ("profile/raw", "profile") -> "raw"
    if base_path not in whole_path:
        raise RuntimeError(base_path + " is not in " + whole_path)
    return whole_path[len(base_path) + 1 :]
