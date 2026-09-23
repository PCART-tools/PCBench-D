def get_sha(pytorch_root: Union[str, Path]) -> str:
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=pytorch_root).decode('ascii').strip()
    except Exception:
        return 'Unknown'
