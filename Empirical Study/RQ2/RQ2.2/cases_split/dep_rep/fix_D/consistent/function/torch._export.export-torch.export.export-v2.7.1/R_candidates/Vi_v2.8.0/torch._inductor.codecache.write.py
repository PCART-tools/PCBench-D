def write(
    content: Union[str, bytes],
    extension: str,
    extra: str = "",
    hash_type: str = "code",
    specified_dir: str = "",
    key: Optional[str] = None,
) -> tuple[str, str]:
    if key is None:
        # use striped content to compute hash so we don't end up with different
        # hashes just because the content begins/ends with different number of
        # spaces.
        key = get_hash(content.strip(), extra, hash_type)
    basename, _subdir, path = get_path(key, extension, specified_dir)
    if not os.path.exists(path):
        write_atomic(path, content, make_dirs=True)
    return basename, path
