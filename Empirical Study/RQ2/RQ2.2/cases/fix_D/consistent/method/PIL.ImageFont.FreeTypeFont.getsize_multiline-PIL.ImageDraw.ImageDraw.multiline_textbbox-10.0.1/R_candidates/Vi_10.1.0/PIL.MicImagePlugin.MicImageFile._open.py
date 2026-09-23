    def _open(self):
        # read the OLE directory and see if this is a likely
        # to be a Microsoft Image Composer file

        try:
            self.ole = olefile.OleFileIO(self.fp)
        except OSError as e:
            msg = "not an MIC file; invalid OLE file"
            raise SyntaxError(msg) from e

        # find ACI subfiles with Image members (maybe not the
        # best way to identify MIC files, but what the... ;-)

        self.images = []
        for path in self.ole.listdir():
            if path[1:] and path[0][-4:] == ".ACI" and path[1] == "Image":
                self.images.append(path)

        # if we didn't find any images, this is probably not
        # an MIC file.
        if not self.images:
            msg = "not an MIC file; no image entries"
            raise SyntaxError(msg)

        self.frame = None
        self._n_frames = len(self.images)
        self.is_animated = self._n_frames > 1

        self.seek(0)
