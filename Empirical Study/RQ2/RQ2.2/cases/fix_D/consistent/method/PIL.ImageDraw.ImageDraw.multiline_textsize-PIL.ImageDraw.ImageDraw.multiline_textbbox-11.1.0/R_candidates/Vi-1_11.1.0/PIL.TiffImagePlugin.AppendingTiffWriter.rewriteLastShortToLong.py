    def rewriteLastShortToLong(self, value: int) -> None:
        self.f.seek(-2, os.SEEK_CUR)
        bytes_written = self.f.write(struct.pack(self.longFmt, value))
        self._verify_bytes_written(bytes_written, 4)
