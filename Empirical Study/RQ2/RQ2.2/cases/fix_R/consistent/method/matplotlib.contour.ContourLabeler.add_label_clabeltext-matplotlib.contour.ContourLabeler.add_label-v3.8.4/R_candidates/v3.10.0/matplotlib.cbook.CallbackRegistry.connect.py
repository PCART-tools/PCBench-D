    def connect(self, signal, func):
        """Register *func* to be called when signal *signal* is generated."""
        if self._signals is not None:
            _api.check_in_list(self._signals, signal=signal)
        proxy = _weak_or_strong_ref(func, functools.partial(self._remove_proxy, signal))
        try:
            return self._func_cid_map[signal, proxy]
        except KeyError:
            cid = self._func_cid_map[signal, proxy] = next(self._cid_gen)
            self.callbacks.setdefault(signal, {})[cid] = proxy
            return cid
