    def _get_head(self) -> bytes:
        version = b"\x2b" if self.bigtiff else b"\x2a"
        if self.endian == "<":
            head = b"II" + version + b"\x00" + o32le(8)
        else:
            head = b"MM\x00" + version + o32be(8)
        if self.bigtiff:
            head += o32le(8) if self.endian == "<" else o32be(8)
            head += b"\x00\x00\x00\x00"
        return head
