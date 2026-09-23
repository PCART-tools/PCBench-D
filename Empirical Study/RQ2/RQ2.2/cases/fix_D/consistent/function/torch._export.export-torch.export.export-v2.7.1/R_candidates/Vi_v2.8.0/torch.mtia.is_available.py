def is_available() -> bool:
    r"""Return true if MTIA device is available"""
    if not _is_compiled():
        return False
    # MTIA has to init devices first to know if there is any devices available.
    return device_count() > 0
