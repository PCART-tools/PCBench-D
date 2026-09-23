    def seek(self, frame):
        if not self._seek_check(frame):
            return
        self.fp = self._fp
        self.offset = self.__mpoffsets[frame]

        self.fp.seek(self.offset + 2)  # skip SOI marker
        segment = self.fp.read(2)
        if not segment:
            msg = "No data found for frame"
            raise ValueError(msg)
        self._size = self._initial_size
        if i16(segment) == 0xFFE1:  # APP1
            n = i16(self.fp.read(2)) - 2
            self.info["exif"] = ImageFile._safe_read(self.fp, n)
            self._reload_exif()

            mptype = self.mpinfo[0xB002][frame]["Attribute"]["MPType"]
            if mptype.startswith("Large Thumbnail"):
                exif = self.getexif().get_ifd(ExifTags.IFD.Exif)
                if 40962 in exif and 40963 in exif:
                    self._size = (exif[40962], exif[40963])
        elif "exif" in self.info:
            del self.info["exif"]
            self._reload_exif()

        self.tile = [("jpeg", (0, 0) + self.size, self.offset, (self.mode, ""))]
        self.__frame = frame
