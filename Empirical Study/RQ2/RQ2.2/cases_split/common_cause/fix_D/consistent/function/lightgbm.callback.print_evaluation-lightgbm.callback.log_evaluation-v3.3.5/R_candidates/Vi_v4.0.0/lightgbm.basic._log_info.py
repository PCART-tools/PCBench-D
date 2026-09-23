def _log_info(msg: str) -> None:
    getattr(_LOGGER, _INFO_METHOD_NAME)(msg)
