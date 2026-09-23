    def __setstate__(self, state):
        self.__dict__ = state
        from .cbook import _InstanceMethodPickler
        if isinstance(self._offset, _InstanceMethodPickler):
            self._offset = self._offset.get_instancemethod()
        self.stale = True
