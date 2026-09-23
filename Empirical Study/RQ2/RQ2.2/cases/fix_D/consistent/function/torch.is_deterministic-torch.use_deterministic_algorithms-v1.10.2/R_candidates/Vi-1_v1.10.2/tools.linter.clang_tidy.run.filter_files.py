def filter_files(files: Iterable[str], file_patterns: Patterns) -> Iterable[str]:
    """Returns all files that match any of the patterns."""
    if VERBOSE:
        log("Filtering with these file patterns: {}".format(file_patterns))
    for file in files:
        if not any(n.match(file) for n in file_patterns.negative):
            if any(p.match(file) for p in file_patterns.positive):
                yield file
                continue
        if VERBOSE:
            log(f"{file} omitted due to file filters")
