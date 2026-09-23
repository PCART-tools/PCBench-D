    def seek(self, frame):
        if not self._seek_check(frame):
            return
        self.frame = frame
        self.fp = self._fp
        self.fp.seek(self._offset[frame])
        PcxImageFile._open(self)
