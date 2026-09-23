    def connect(self, s, func):
        """Register *func* to be called when signal *s* is generated.
        """
        self._func_cid_map.setdefault(s, {})
        try:
            proxy = WeakMethod(func, self._remove_proxy)
        except TypeError:
            proxy = _StrongRef(func)
        if proxy in self._func_cid_map[s]:
            return self._func_cid_map[s][proxy]

        cid = next(self._cid_gen)
        self._func_cid_map[s][proxy] = cid
        self.callbacks.setdefault(s, {})
        self.callbacks[s][cid] = proxy
        return cid
