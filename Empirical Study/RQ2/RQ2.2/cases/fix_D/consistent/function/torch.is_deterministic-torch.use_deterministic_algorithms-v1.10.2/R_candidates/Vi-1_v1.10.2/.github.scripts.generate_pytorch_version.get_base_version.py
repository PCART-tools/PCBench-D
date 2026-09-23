def get_base_version() -> str:
    root = get_pytorch_root()
    dirty_version = open(root / 'version.txt', 'r').read().strip()
    # Strips trailing a0 from version.txt, not too sure why it's there in the
    # first place
    return re.sub(LEGACY_BASE_VERSION_SUFFIX_PATTERN, "", dirty_version)
