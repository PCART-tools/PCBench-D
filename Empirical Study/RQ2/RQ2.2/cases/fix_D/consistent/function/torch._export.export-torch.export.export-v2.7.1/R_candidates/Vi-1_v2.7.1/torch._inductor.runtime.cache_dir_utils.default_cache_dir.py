def default_cache_dir() -> str:
    sanitized_username = re.sub(r'[\\/:*?"<>|]', "_", getpass.getuser())
    return os.path.join(
        tempfile.gettempdir(),
        "torchinductor_" + sanitized_username,
    )
