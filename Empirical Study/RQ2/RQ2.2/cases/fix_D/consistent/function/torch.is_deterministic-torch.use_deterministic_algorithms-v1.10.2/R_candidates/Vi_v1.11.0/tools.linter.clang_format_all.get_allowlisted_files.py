def get_allowlisted_files() -> Set[str]:
    """
    Parse CLANG_FORMAT_ALLOWLIST and resolve all directories.
    Returns the set of allowlist cpp source files.
    """
    matches = []
    for dir in CLANG_FORMAT_ALLOWLIST:
        for root, dirnames, filenames in os.walk(dir):
            for filename in filenames:
                if CPP_FILE_REGEX.match(filename):
                    matches.append(os.path.join(root, filename))
    return set(matches)
