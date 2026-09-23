    def _remove_proxy(self, signal, proxy, *, _is_finalizing=sys.is_finalizing):
        if _is_finalizing():
            # Weakrefs can't be properly torn down at that point anymore.
            return
        cid = self._func_cid_map.pop((signal, proxy), None)
        if cid is not None:
            del self.callbacks[signal][cid]
            self._pickled_cids.discard(cid)
        else:  # Not found
            return
        if len(self.callbacks[signal]) == 0:  # Clean up empty dicts
            del self.callbacks[signal]
