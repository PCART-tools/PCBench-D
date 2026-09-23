    def _load(self) -> None:
        self._compression, self._encoding, alpha = self.args

        if self._compression == Format.JPEG:
            self._decode_jpeg_stream()

        elif self._compression == 1:
            if self._encoding in (4, 5):
                palette = self._read_palette()
                data = self._read_bgra(palette, alpha)
                self.set_as_raw(data)
            else:
                msg = f"Unsupported BLP encoding {repr(self._encoding)}"
                raise BLPFormatError(msg)
        else:
            msg = f"Unsupported BLP compression {repr(self._encoding)}"
            raise BLPFormatError(msg)
