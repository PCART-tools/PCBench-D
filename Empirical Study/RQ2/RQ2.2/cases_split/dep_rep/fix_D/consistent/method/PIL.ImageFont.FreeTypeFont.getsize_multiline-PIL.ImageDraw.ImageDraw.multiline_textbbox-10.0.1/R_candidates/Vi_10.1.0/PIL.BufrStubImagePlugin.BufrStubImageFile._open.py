    def _open(self):
        offset = self.fp.tell()

        if not _accept(self.fp.read(4)):
            msg = "Not a BUFR file"
            raise SyntaxError(msg)

        self.fp.seek(offset)

        # make something up
        self._mode = "F"
        self._size = 1, 1

        loader = self._load()
        if loader:
            loader.open(self)
