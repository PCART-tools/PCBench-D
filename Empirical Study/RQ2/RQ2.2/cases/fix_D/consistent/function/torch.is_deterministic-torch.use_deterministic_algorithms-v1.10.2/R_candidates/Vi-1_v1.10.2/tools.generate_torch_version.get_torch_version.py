def get_torch_version(sha: Optional[str] = None) -> str:
    pytorch_root = Path(__file__).parent.parent
    version = open(pytorch_root / 'version.txt', 'r').read().strip()

    if os.getenv('PYTORCH_BUILD_VERSION'):
        assert os.getenv('PYTORCH_BUILD_NUMBER') is not None
        build_number = int(os.getenv('PYTORCH_BUILD_NUMBER', ""))
        version = os.getenv('PYTORCH_BUILD_VERSION', "")
        if build_number > 1:
            version += '.post' + str(build_number)
    elif sha != 'Unknown':
        if sha is None:
            sha = get_sha(pytorch_root)
        version += '+git' + sha[:7]
    return version
