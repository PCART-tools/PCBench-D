    def _open(self) -> None:
        # Header
        s = self.fp.read(4)
        if not _accept(s):
            msg = "not a DCX file"
            raise SyntaxError(msg)

        # Component directory
        self._offset = []
        for i in range(1024):
            offset = i32(self.fp.read(4))
            if not offset:
                break
            self._offset.append(offset)

        self._fp = self.fp
        self.frame = -1
        self.n_frames = len(self._offset)
        self.is_animated = self.n_frames > 1
        self.seek(0)
