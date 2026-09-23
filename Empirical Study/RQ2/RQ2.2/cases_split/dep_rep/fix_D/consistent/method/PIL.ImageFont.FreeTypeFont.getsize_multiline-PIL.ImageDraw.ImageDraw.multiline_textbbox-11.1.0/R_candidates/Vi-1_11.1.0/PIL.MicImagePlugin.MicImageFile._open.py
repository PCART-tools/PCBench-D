    def _open(self) -> None:
        # read the OLE directory and see if this is a likely
        # to be a Microsoft Image Composer file

        try:
            self.ole = olefile.OleFileIO(self.fp)
        except OSError as e:
            msg = "not an MIC file; invalid OLE file"
            raise SyntaxError(msg) from e

        # find ACI subfiles with Image members (maybe not the
        # best way to identify MIC files, but what the... ;-)

        self.images = [
            path
            for path in self.ole.listdir()
            if path[1:] and path[0][-4:] == ".ACI" and path[1] == "Image"
        ]

        # if we didn't find any images, this is probably not
        # an MIC file.
        if not self.images:
            msg = "not an MIC file; no image entries"
            raise SyntaxError(msg)

        self.frame = -1
        self._n_frames = len(self.images)
        self.is_animated = self._n_frames > 1

        self.__fp = self.fp
        self.seek(0)
