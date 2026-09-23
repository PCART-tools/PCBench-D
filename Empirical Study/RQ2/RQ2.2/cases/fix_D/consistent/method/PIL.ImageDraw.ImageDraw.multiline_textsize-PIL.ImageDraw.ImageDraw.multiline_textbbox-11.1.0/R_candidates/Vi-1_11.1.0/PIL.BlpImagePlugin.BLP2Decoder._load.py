    def _load(self) -> None:
        self._compression, self._encoding, alpha, self._alpha_encoding = self.args

        palette = self._read_palette()

        assert self.fd is not None
        self.fd.seek(self._offsets[0])

        if self._compression == 1:
            # Uncompressed or DirectX compression

            if self._encoding == Encoding.UNCOMPRESSED:
                data = self._read_bgra(palette, alpha)

            elif self._encoding == Encoding.DXT:
                data = bytearray()
                if self._alpha_encoding == AlphaEncoding.DXT1:
                    linesize = (self.state.xsize + 3) // 4 * 8
                    for yb in range((self.state.ysize + 3) // 4):
                        for d in decode_dxt1(self._safe_read(linesize), alpha):
                            data += d

                elif self._alpha_encoding == AlphaEncoding.DXT3:
                    linesize = (self.state.xsize + 3) // 4 * 16
                    for yb in range((self.state.ysize + 3) // 4):
                        for d in decode_dxt3(self._safe_read(linesize)):
                            data += d

                elif self._alpha_encoding == AlphaEncoding.DXT5:
                    linesize = (self.state.xsize + 3) // 4 * 16
                    for yb in range((self.state.ysize + 3) // 4):
                        for d in decode_dxt5(self._safe_read(linesize)):
                            data += d
                else:
                    msg = f"Unsupported alpha encoding {repr(self._alpha_encoding)}"
                    raise BLPFormatError(msg)
            else:
                msg = f"Unknown BLP encoding {repr(self._encoding)}"
                raise BLPFormatError(msg)

        else:
            msg = f"Unknown BLP compression {repr(self._compression)}"
            raise BLPFormatError(msg)

        self.set_as_raw(data)
