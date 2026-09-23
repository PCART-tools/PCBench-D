def _log_callback(msg: bytes) -> None:
    """Redirect logs from native library into Python."""
    _log_native(str(msg.decode('utf-8')))
