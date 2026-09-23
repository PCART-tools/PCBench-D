    def __setstate__(self, state):
        # for pickle compat.
        self._tz = state['tz']
        self._unit = state['unit']
