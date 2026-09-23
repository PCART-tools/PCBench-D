    def _load(self):
        if self._blp_compression == Format.JPEG:
            self._decode_jpeg_stream()

        elif self._blp_compression == 1:
            if self._blp_encoding in (4, 5):
                palette = self._read_palette()
                data = self._read_bgra(palette)
                self.set_as_raw(bytes(data))
            else:
                msg = f"Unsupported BLP encoding {repr(self._blp_encoding)}"
                raise BLPFormatError(msg)
        else:
            msg = f"Unsupported BLP compression {repr(self._blp_encoding)}"
            raise BLPFormatError(msg)
