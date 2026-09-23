    def _seek(self, frame: int) -> None:
        if self.__physical_frame == frame:
            return  # Nothing to do
        if frame < self.__physical_frame:
            self._reset()  # Rewind to beginning
        while self.__physical_frame < frame:
            self._get_next()  # Advance to the requested frame
