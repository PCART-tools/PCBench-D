    @_api.rename_parameter("3.4", "s", "signal")
    def connect(self, signal, func):
        """Register *func* to be called when signal *signal* is generated."""
        if signal == "units finalize":
            _api.warn_deprecated(
                "3.5", name=signal, obj_type="signal", alternative="units")
        self._func_cid_map.setdefault(signal, {})
        proxy = _weak_or_strong_ref(func, self._remove_proxy)
        if proxy in self._func_cid_map[signal]:
            return self._func_cid_map[signal][proxy]
        cid = next(self._cid_gen)
        self._func_cid_map[signal][proxy] = cid
        self.callbacks.setdefault(signal, {})
        self.callbacks[signal][cid] = proxy
        return cid
