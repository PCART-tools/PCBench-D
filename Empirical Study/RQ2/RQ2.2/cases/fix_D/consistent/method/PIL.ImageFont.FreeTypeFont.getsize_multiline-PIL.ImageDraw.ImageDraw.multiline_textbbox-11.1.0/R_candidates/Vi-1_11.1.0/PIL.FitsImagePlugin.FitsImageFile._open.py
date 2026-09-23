    def _open(self) -> None:
        assert self.fp is not None

        headers: dict[bytes, bytes] = {}
        header_in_progress = False
        decoder_name = ""
        while True:
            header = self.fp.read(80)
            if not header:
                msg = "Truncated FITS file"
                raise OSError(msg)
            keyword = header[:8].strip()
            if keyword in (b"SIMPLE", b"XTENSION"):
                header_in_progress = True
            elif headers and not header_in_progress:
                # This is now a data unit
                break
            elif keyword == b"END":
                # Seek to the end of the header unit
                self.fp.seek(math.ceil(self.fp.tell() / 2880) * 2880)
                if not decoder_name:
                    decoder_name, offset, args = self._parse_headers(headers)

                header_in_progress = False
                continue

            if decoder_name:
                # Keep going to read past the headers
                continue

            value = header[8:].split(b"/")[0].strip()
            if value.startswith(b"="):
                value = value[1:].strip()
            if not headers and (not _accept(keyword) or value != b"T"):
                msg = "Not a FITS file"
                raise SyntaxError(msg)
            headers[keyword] = value

        if not decoder_name:
            msg = "No image data"
            raise ValueError(msg)

        offset += self.fp.tell() - 80
        self.tile = [ImageFile._Tile(decoder_name, (0, 0) + self.size, offset, args)]
