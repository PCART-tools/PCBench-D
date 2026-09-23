    def _open(self):
        offset = self.fp.tell()

        if not _accept(self.fp.read(8)):
            msg = "Not an HDF file"
            raise SyntaxError(msg)

        self.fp.seek(offset)

        # make something up
        self.mode = "F"
        self._size = 1, 1

        loader = self._load()
        if loader:
            loader.open(self)
