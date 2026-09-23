    def _remove_proxy(self, proxy):
        for signal, proxies in list(self._func_cid_map.items()):
            try:
                del self.callbacks[signal][proxies[proxy]]
            except KeyError:
                pass
            if len(self.callbacks[signal]) == 0:
                del self.callbacks[signal]
                del self._func_cid_map[signal]
