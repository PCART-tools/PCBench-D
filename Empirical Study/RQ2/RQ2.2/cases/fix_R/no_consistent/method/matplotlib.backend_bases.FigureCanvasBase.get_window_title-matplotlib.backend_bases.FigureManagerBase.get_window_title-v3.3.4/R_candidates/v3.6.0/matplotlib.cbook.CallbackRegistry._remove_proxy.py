    def _remove_proxy(self, proxy, *, _is_finalizing=sys.is_finalizing):
        if _is_finalizing():
            # Weakrefs can't be properly torn down at that point anymore.
            return
        for signal, proxy_to_cid in list(self._func_cid_map.items()):
            cid = proxy_to_cid.pop(proxy, None)
            if cid is not None:
                del self.callbacks[signal][cid]
                self._pickled_cids.discard(cid)
                break
        else:
            # Not found
            return
        # Clean up empty dicts
        if len(self.callbacks[signal]) == 0:
            del self.callbacks[signal]
            del self._func_cid_map[signal]
