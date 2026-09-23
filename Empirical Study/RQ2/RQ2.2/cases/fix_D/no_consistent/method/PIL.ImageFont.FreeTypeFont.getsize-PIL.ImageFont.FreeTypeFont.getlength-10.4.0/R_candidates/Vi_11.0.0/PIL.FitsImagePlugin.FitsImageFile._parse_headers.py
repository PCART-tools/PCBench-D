    def _parse_headers(
        self, headers: dict[bytes, bytes]
    ) -> tuple[str, int, tuple[str | int, ...]]:
        prefix = b""
        decoder_name = "raw"
        offset = 0
        if (
            headers.get(b"XTENSION") == b"'BINTABLE'"
            and headers.get(b"ZIMAGE") == b"T"
            and headers[b"ZCMPTYPE"] == b"'GZIP_1  '"
        ):
            no_prefix_size = self._get_size(headers, prefix) or (0, 0)
            number_of_bits = int(headers[b"BITPIX"])
            offset = no_prefix_size[0] * no_prefix_size[1] * (number_of_bits // 8)

            prefix = b"Z"
            decoder_name = "fits_gzip"

        size = self._get_size(headers, prefix)
        if not size:
            return "", 0, ()

        self._size = size

        number_of_bits = int(headers[prefix + b"BITPIX"])
        if number_of_bits == 8:
            self._mode = "L"
        elif number_of_bits == 16:
            self._mode = "I;16"
        elif number_of_bits == 32:
            self._mode = "I"
        elif number_of_bits in (-32, -64):
            self._mode = "F"

        args: tuple[str | int, ...]
        if decoder_name == "raw":
            args = (self.mode, 0, -1)
        else:
            args = (number_of_bits,)
        return decoder_name, offset, args
