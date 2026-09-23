    def disconnect(self, cid):
        """
        Disconnect the callback registered with callback id *cid*.

        No error is raised if such a callback does not exist.
        """
        self._pickled_cids.discard(cid)
        for signal, proxy in self._func_cid_map:
            if self._func_cid_map[signal, proxy] == cid:
                break
        else:  # Not found
            return
        assert self.callbacks[signal][cid] == proxy
        del self.callbacks[signal][cid]
        self._func_cid_map.pop((signal, proxy))
        if len(self.callbacks[signal]) == 0:  # Clean up empty dicts
            del self.callbacks[signal]
