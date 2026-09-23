    def _release_acquired(self, key, transport):
        if self._closed:
            # acquired connection is already released on connector closing
            return

        acquired = self._acquired[key]
        try:
            acquired.remove(transport)
        except KeyError:  # pragma: no cover
            # this may be result of undetermenistic order of objects
            # finalization due garbage collection.
            return None

        return acquired
