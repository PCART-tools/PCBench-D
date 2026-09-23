    def seek(self, frame):
        if not self._seek_check(frame):
            return
        self.fp = self._fp
        self.offset = self.__mpoffsets[frame]

        original_exif = self.info.get("exif")
        if "exif" in self.info:
            del self.info["exif"]

        self.fp.seek(self.offset + 2)  # skip SOI marker
        if not self.fp.read(2):
            msg = "No data found for frame"
            raise ValueError(msg)
        self.fp.seek(self.offset)
        JpegImagePlugin.JpegImageFile._open(self)
        if self.info.get("exif") != original_exif:
            self._reload_exif()

        self.tile = [("jpeg", (0, 0) + self.size, self.offset, self.tile[0][-1])]
        self.__frame = frame
