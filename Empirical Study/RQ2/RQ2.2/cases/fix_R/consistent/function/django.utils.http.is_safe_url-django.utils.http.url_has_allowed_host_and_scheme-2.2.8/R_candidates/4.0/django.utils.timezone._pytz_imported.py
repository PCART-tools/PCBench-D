def _pytz_imported():
    """
    Detects whether or not pytz has been imported without importing pytz.

    Copied from pytz_deprecation_shim with thanks to Paul Ganssle.
    """
    global _PYTZ_IMPORTED

    if not _PYTZ_IMPORTED and "pytz" in sys.modules:
        _PYTZ_IMPORTED = True

    return _PYTZ_IMPORTED
