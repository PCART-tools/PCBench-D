def _mkdir_p(d: str) -> None:
    try:
        os.makedirs(d)
    except OSError:
        pass
