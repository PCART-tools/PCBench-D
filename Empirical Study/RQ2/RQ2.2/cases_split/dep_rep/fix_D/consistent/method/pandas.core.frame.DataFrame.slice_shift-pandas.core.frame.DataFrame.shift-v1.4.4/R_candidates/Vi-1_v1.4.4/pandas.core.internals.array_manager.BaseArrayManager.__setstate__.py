    def __setstate__(self, state):
        self.arrays = state[0]
        self._axes = state[1]
