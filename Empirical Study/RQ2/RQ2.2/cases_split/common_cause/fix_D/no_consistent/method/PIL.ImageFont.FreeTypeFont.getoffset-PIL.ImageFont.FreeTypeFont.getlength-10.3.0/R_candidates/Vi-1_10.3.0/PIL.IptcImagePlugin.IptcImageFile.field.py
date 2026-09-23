    def field(self) -> tuple[tuple[int, int] | None, int]:
        #
        # get a IPTC field header
        s = self.fp.read(5)
        if not s.strip(b"\x00"):
            return None, 0

        tag = s[1], s[2]

        # syntax
        if s[0] != 0x1C or tag[0] not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 240]:
            msg = "invalid IPTC/NAA file"
            raise SyntaxError(msg)

        # field size
        size = s[3]
        if size > 132:
            msg = "illegal field length in IPTC/NAA file"
            raise OSError(msg)
        elif size == 128:
            size = 0
        elif size > 128:
            size = _i(self.fp.read(size - 128))
        else:
            size = i16(s, 3)

        return tag, size
