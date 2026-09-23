def get_file_patterns(globs: Iterable[str], regexes: Iterable[str]) -> Patterns:
    """Returns a list of compiled regex objects from globs and regex pattern strings."""
    # fnmatch.translate converts a glob into a regular expression.
    # https://docs.python.org/2/library/fnmatch.html#fnmatch.translate
    glob = split_negative_from_positive_patterns(globs)
    regexes_ = split_negative_from_positive_patterns(regexes)

    positive_regexes = regexes_.positive + [fnmatch.translate(g) for g in glob.positive]
    negative_regexes = regexes_.negative + [fnmatch.translate(g) for g in glob.negative]

    positive_patterns = [re.compile(regex) for regex in positive_regexes] or [
        DEFAULT_FILE_PATTERN
    ]
    negative_patterns = [re.compile(regex) for regex in negative_regexes]

    return Patterns(positive_patterns, negative_patterns)
