def read_config(config_path: Path) -> Set[str]:
    """
    Return the set of `files` in the `mypy` ini file at config_path.
    """
    config = ConfigParser()
    config.read(config_path)
    # hopefully on Windows this gives posix paths
    return set(mypy.config_parser.split_and_match_files(
        config['mypy']['files'],
    ))
