    def __setstate__(self, state):
        self.__dict__ = state
        # layoutboxes don't survive pickling...
        self._layoutbox = None
