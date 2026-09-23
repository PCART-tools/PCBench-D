    def _open(self) -> None:
        if not _accept(self.fp.read(4)):
            msg = "Not a BUFR file"
            raise SyntaxError(msg)

        self.fp.seek(-4, os.SEEK_CUR)

        # make something up
        self._mode = "F"
        self._size = 1, 1

        loader = self._load()
        if loader:
            loader.open(self)
