def echo2(msg: str, fail: bool = False) -> str:
    """
    returns ``msg`` or raises a RuntimeError if ``fail`` is set
    """
    if fail:
        raise RuntimeError(msg)
    return msg
