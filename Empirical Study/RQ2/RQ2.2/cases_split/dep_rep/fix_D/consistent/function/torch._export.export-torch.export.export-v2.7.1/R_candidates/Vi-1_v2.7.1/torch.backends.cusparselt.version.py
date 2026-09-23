def version() -> Optional[int]:
    """Return the version of cuSPARSELt"""
    if not _init():
        return None
    return __cusparselt_version
