def _log_warning(msg: str) -> None:
    getattr(_LOGGER, _WARNING_METHOD_NAME)(msg)
