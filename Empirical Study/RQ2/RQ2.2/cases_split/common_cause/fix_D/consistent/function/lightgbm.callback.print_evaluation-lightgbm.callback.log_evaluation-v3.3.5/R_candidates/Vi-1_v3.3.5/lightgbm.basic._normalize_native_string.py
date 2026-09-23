def _normalize_native_string(func: Callable[[str], None]) -> Callable[[str], None]:
    """Join log messages from native library which come by chunks."""
    msg_normalized: List[str] = []

    @wraps(func)
    def wrapper(msg: str) -> None:
        nonlocal msg_normalized
        if msg.strip() == '':
            msg = ''.join(msg_normalized)
            msg_normalized = []
            return func(msg)
        else:
            msg_normalized.append(msg)

    return wrapper
