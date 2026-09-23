def config_files() -> Dict[str, Set[str]]:
    """
    Return a dict from all our `mypy` ini filenames to their `files`.
    """
    return {str(ini): read_config(ini) for ini in Path().glob('mypy*.ini')}
