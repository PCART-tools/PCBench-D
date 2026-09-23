    def seek(self, frame):
        if not self._seek_check(frame):
            return
        if frame < self.__frame:
            self._seek(0)

        for f in range(self.__frame + 1, frame + 1):
            self._seek(f)
