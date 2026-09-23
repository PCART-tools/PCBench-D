    def rewriteLastShort(self, value: int) -> None:
        self.f.seek(-2, os.SEEK_CUR)
        bytes_written = self.f.write(struct.pack(self.shortFmt, value))
        if bytes_written is not None and bytes_written != 2:
            msg = f"wrote only {bytes_written} bytes but wanted 2"
            raise RuntimeError(msg)
