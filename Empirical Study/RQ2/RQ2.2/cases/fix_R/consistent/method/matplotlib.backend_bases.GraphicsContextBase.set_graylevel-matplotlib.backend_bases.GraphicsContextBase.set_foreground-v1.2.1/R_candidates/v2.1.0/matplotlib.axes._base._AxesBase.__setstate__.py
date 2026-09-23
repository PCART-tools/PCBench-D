    def __setstate__(self, state):
        self.__dict__ = state
        # put the _remove_method back on all artists contained within the axes
        for container_name in ['lines', 'collections', 'tables', 'patches',
                               'texts', 'images']:
            container = getattr(self, container_name)
            for artist in container:
                artist._remove_method = container.remove
        self._stale = True
