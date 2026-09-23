    def disconnect(self, cid):
        """
        Disconnect the callback registered with callback id *cid*.

        No error is raised if such a callback does not exist.
        """
        self._pickled_cids.discard(cid)
        # Clean up callbacks
        for signal, cid_to_proxy in list(self.callbacks.items()):
            proxy = cid_to_proxy.pop(cid, None)
            if proxy is not None:
                break
        else:
            # Not found
            return

        proxy_to_cid = self._func_cid_map[signal]
        for current_proxy, current_cid in list(proxy_to_cid.items()):
            if current_cid == cid:
                assert proxy is current_proxy
                del proxy_to_cid[current_proxy]
        # Clean up empty dicts
        if len(self.callbacks[signal]) == 0:
            del self.callbacks[signal]
            del self._func_cid_map[signal]
