def _import_lazy():
    global _LAZY_IMPORTED_DYNDEPS
    if not _LAZY_IMPORTED_DYNDEPS:
        return
    for name in list(_LAZY_IMPORTED_DYNDEPS):
        try:
            dyndep.InitOpLibrary(name, trigger_lazy=False)
        except BaseException as e:
            if _error_handler:
                _error_handler(e)
        finally:
            _LAZY_IMPORTED_DYNDEPS.remove(name)
