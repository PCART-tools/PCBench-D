    def seek(self, frame: int) -> None:
        """Select a given frame as current image"""
        if not self._seek_check(frame):
            return
        self._seek(frame)
        # Create a new core image object on second and
        # subsequent frames in the image. Image may be
        # different size/mode.
        Image._decompression_bomb_check(self.size)
        self.im = Image.core.new(self.mode, self.size)
