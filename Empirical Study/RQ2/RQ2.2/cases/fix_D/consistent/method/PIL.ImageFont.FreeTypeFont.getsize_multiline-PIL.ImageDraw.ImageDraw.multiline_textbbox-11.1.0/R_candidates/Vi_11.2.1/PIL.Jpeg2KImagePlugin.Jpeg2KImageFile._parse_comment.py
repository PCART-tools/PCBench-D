    def _parse_comment(self) -> None:
        while True:
            marker = self.fp.read(2)
            if not marker:
                break
            typ = marker[1]
            if typ in (0x90, 0xD9):
                # Start of tile or end of codestream
                break
            hdr = self.fp.read(2)
            length = _binary.i16be(hdr)
            if typ == 0x64:
                # Comment
                self.info["comment"] = self.fp.read(length - 2)[2:]
                break
            else:
                self.fp.seek(length - 2, os.SEEK_CUR)
