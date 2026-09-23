def update_set() -> None:
    for file_name in covered_lines:
        # difference_update
        uncovered_lines[file_name].difference_update(covered_lines[file_name])
