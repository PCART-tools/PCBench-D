def parse_version(version: str) -> Version:
    """
    Parses a version string into (major, minor, patch) version numbers.

    Args:
      version: Full version number string, possibly including revision / commit hash.

    Returns:
      An int 3-tuple of (major, minor, patch) version numbers.
    """
    # Extract version number part (i.e. toss any revision / hash parts).
    version_number_str = version
    for i in range(len(version)):
        c = version[i]
        if not (c.isdigit() or c == "."):
            version_number_str = version[:i]
            break

    return cast(Version, tuple([int(n) for n in version_number_str.split(".")]))
