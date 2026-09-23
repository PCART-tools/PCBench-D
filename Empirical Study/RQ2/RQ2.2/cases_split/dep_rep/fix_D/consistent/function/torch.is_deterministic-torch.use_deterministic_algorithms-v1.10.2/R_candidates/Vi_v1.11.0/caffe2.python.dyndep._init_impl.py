def _init_impl(path, trigger_lazy=True):
    with dll_lock:
        _IMPORTED_DYNDEPS.add(path)
        with extension_loader.DlopenGuard():
            ctypes.CDLL(path)
        # reinitialize available ops
        core.RefreshRegisteredOperators(trigger_lazy)
