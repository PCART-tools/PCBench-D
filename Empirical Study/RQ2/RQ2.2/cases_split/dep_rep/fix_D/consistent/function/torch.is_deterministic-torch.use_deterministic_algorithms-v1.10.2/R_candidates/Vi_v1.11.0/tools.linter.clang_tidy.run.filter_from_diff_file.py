def filter_from_diff_file(
    paths: List[str], filename: str
) -> Tuple[List[str], List[Dict[Any, Any]]]:
    with open(filename, "r") as f:
        diff = f.read()
    return filter_from_diff(paths, [diff])
