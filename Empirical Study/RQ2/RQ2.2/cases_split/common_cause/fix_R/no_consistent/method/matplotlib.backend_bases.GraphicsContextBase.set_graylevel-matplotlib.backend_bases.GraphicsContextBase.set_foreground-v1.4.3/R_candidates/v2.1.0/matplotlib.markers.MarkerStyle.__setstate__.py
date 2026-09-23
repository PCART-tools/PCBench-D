    def __setstate__(self, statedict):
        self.__dict__ = statedict
        self.set_marker(self._marker)
