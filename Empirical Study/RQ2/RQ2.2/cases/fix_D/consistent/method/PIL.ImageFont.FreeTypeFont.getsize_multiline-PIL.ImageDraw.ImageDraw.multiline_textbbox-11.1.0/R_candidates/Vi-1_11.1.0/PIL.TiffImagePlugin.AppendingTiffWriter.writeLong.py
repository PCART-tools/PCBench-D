    def writeLong(self, value: int) -> None:
        bytes_written = self.f.write(struct.pack(self.longFmt, value))
        self._verify_bytes_written(bytes_written, 4)
