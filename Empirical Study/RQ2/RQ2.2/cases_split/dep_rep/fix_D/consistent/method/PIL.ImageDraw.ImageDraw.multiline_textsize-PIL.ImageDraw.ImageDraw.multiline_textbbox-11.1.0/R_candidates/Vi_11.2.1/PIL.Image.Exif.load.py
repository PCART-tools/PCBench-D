    def load(self, data: bytes) -> None:
        # Extract EXIF information.  This is highly experimental,
        # and is likely to be replaced with something better in a future
        # version.

        # The EXIF record consists of a TIFF file embedded in a JPEG
        # application marker (!).
        if data == self._loaded_exif:
            return
        self._loaded_exif = data
        self._data.clear()
        self._hidden_data.clear()
        self._ifds.clear()
        while data and data.startswith(b"Exif\x00\x00"):
            data = data[6:]
        if not data:
            self._info = None
            return

        self.fp: IO[bytes] = io.BytesIO(data)
        self.head = self.fp.read(8)
        # process dictionary
        from . import TiffImagePlugin

        self._info = TiffImagePlugin.ImageFileDirectory_v2(self.head)
        self.endian = self._info._endian
        self.fp.seek(self._info.next)
        self._info.load(self.fp)
