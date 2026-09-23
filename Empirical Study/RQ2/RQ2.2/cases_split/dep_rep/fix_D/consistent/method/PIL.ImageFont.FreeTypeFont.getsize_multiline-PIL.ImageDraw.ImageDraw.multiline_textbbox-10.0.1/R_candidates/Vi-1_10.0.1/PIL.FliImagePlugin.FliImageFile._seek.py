    def _seek(self, frame):
        if frame == 0:
            self.__frame = -1
            self._fp.seek(self.__rewind)
            self.__offset = 128
        else:
            # ensure that the previous frame was loaded
            self.load()

        if frame != self.__frame + 1:
            msg = f"cannot seek to frame {frame}"
            raise ValueError(msg)
        self.__frame = frame

        # move to next frame
        self.fp = self._fp
        self.fp.seek(self.__offset)

        s = self.fp.read(4)
        if not s:
            raise EOFError

        framesize = i32(s)

        self.decodermaxblock = framesize
        self.tile = [("fli", (0, 0) + self.size, self.__offset, None)]

        self.__offset += framesize
