def enable_minidumps(directory=DEFAULT_MINIDUMP_DIR):
    if directory == DEFAULT_MINIDUMP_DIR:
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
    elif not os.path.exists(directory):
        raise RuntimeError(f"Directory does not exist: {directory}")

    torch._C._enable_minidumps(directory)
