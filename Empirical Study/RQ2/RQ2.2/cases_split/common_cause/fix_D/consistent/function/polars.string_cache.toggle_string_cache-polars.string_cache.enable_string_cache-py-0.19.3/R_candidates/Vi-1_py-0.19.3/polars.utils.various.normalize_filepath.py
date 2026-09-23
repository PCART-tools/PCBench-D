def normalize_filepath(path: str | Path, *, check_not_directory: bool = True) -> str:
    """Create a string path, expanding the home directory if present."""
    # don't use pathlib here as it modifies slashes (s3:// -> s3:/)
    path = os.path.expanduser(path)  # noqa: PTH111
    if (
        check_not_directory
        and os.path.exists(path)  # noqa: PTH110
        and os.path.isdir(path)  # noqa: PTH112
    ):
        raise IsADirectoryError(f"expected a file path; {path!r} is a directory")
    return path
