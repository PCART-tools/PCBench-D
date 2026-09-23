def get_recursive_files(folder: str, extension: str) -> Iterable[str]:
    """
    Get recursive list of files with given extension even.

    Use it instead of glob(os.path.join(folder, '**', f'*{extension}'))
    if folder/file names can start with `.`, which makes it hidden on Unix platforms
    """
    assert extension.startswith(".")
    for root, _, files in os.walk(folder):
        for fname in files:
            if os.path.splitext(fname)[1] == extension:
                yield os.path.join(root, fname)
