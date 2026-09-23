    def _release_acquired(self, key, proto):
        if self._closed:
            # acquired connection is already released on connector closing
            return

        try:
            self._acquired.remove(proto)
            self._acquired_per_host[key].remove(proto)
            if not self._acquired_per_host[key]:
                del self._acquired_per_host[key]
        except KeyError:  # pragma: no cover
            # this may be result of undetermenistic order of objects
            # finalization due garbage collection.
            pass
        else:
            self._release_waiter()
