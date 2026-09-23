    def connect(self, s, func):
        """
        register *func* to be called when a signal *s* is generated
        func will be called
        """
        self._func_cid_map.setdefault(s, WeakKeyDictionary())
        # Note proxy not needed in python 3.
        # TODO rewrite this when support for python2.x gets dropped.
        proxy = _BoundMethodProxy(func)
        if proxy in self._func_cid_map[s]:
            return self._func_cid_map[s][proxy]

        proxy.add_destroy_callback(self._remove_proxy)
        self._cid += 1
        cid = self._cid
        self._func_cid_map[s][proxy] = cid
        self.callbacks.setdefault(s, dict())
        self.callbacks[s][cid] = proxy
        return cid
