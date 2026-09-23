    def seek(self, frame: int) -> None:
        """Select a given frame as current image"""
        if not self._seek_check(frame):
            return
        self._seek(frame)
        if self._im is not None and (
            self.im.size != self._tile_size or self.im.mode != self.mode
        ):
            # The core image will no longer be used
            self._im = None
