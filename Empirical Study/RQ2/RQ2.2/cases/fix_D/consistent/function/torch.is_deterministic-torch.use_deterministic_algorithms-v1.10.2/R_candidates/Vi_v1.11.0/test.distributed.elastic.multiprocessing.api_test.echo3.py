def echo3(msg: str, fail: bool = False) -> str:
    """
    returns ``msg`` or induces a SIGSEGV if ``fail`` is set
    """
    if fail:
        ctypes.string_at(0)
    return msg
