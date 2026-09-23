def filter_from_diff(
    paths: List[str], diffs: List[str]
) -> Tuple[List[str], List[Dict[Any, Any]]]:
    files = []
    line_filters = []

    for diff in diffs:
        changed_files = find_changed_lines(diff)
        changed_files = {
            filename: v
            for filename, v in changed_files.items()
            if any(filename.startswith(path) for path in paths)
        }
        line_filters += [
            {"name": name, "lines": lines} for name, lines, in changed_files.items()
        ]
        files += list(changed_files.keys())

    return files, line_filters
