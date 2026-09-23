def _mkdir_p(d: str) -> None:
    try:
        os.makedirs(d, exist_ok=True)
    except OSError as e:
        raise RuntimeError(f"Failed to create folder {os.path.abspath(d)}: {e.strerror}") from e
