def _check_if_delta_available() -> None:
    if not _DELTALAKE_AVAILABLE:
        raise ModuleNotFoundError(
            "deltalake is not installed"
            "\n\nPlease run: `pip install deltalake>=0.9.0`"
        )
