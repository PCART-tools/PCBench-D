    def writeShort(self, value: int) -> None:
        bytes_written = self.f.write(struct.pack(self.shortFmt, value))
        self._verify_bytes_written(bytes_written, 2)
