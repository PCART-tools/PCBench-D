    def seek(self, frame: int) -> None:
        if not self._seek_check(frame):
            return

        # Set tile
        self.__frame = frame
        self.tile = [ImageFile._Tile("raw", (0, 0) + self.size, 0, self.mode)]
