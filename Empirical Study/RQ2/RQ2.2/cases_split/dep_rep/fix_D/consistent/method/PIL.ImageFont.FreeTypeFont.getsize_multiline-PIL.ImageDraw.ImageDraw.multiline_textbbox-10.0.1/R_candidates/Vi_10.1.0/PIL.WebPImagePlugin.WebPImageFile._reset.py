    def _reset(self, reset=True):
        if reset:
            self._decoder.reset()
        self.__physical_frame = 0
        self.__loaded = -1
        self.__timestamp = 0
