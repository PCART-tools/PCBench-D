def warn_if_tmpdir_set(env: Dict[str, str]) -> None:
    """
    Warn the user that setting TMPDIR with fast_nvcc might not work.
    """
    if os.getenv('TMPDIR') or 'TMPDIR' in env:
        fast_nvcc_warn("TMPDIR is set, might not work; see this URL:")
        fast_nvcc_warn(url_vars)
