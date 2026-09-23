def split_path(path: str) -> List[str]:
    """
    Split a relative (not absolute) POSIX path into its segments.
    """
    pure = PurePosixPath(path)
    return [str(p.name) for p in list(reversed(pure.parents))[1:] + [pure]]
