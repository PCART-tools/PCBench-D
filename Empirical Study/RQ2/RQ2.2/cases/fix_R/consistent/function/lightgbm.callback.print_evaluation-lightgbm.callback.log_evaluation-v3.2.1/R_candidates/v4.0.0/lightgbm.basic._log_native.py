@_normalize_native_string
def _log_native(msg: str) -> None:
    getattr(_LOGGER, _INFO_METHOD_NAME)(msg)
