    def _open(self) -> None:
        #
        # read the OLE directory and see if this is a likely
        # to be a FlashPix file

        try:
            self.ole = olefile.OleFileIO(self.fp)
        except OSError as e:
            msg = "not an FPX file; invalid OLE file"
            raise SyntaxError(msg) from e

        root = self.ole.root
        if not root or root.clsid != "56616700-C154-11CE-8553-00AA00A1F95B":
            msg = "not an FPX file; bad root CLSID"
            raise SyntaxError(msg)

        self._open_index(1)
