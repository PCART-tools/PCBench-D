def get_pytorch_root() -> Path:
    return Path(subprocess.check_output(
        ['git', 'rev-parse', '--show-toplevel']
    ).decode('ascii').strip())
