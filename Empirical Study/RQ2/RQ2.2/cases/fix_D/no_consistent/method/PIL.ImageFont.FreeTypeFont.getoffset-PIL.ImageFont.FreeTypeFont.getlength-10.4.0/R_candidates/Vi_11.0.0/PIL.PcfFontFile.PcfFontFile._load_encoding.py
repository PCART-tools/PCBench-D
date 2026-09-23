    def _load_encoding(self) -> list[int | None]:
        fp, format, i16, i32 = self._getformat(PCF_BDF_ENCODINGS)

        first_col, last_col = i16(fp.read(2)), i16(fp.read(2))
        first_row, last_row = i16(fp.read(2)), i16(fp.read(2))

        i16(fp.read(2))  # default

        nencoding = (last_col - first_col + 1) * (last_row - first_row + 1)

        # map character code to bitmap index
        encoding: list[int | None] = [None] * min(256, nencoding)

        encoding_offsets = [i16(fp.read(2)) for _ in range(nencoding)]

        for i in range(first_col, len(encoding)):
            try:
                encoding_offset = encoding_offsets[
                    ord(bytearray([i]).decode(self.charset_encoding))
                ]
                if encoding_offset != 0xFFFF:
                    encoding[i] = encoding_offset
            except UnicodeDecodeError:
                # character is not supported in selected encoding
                pass

        return encoding
