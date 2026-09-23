    def rewriteLastShortToLong(self, value: int) -> None:
        self.f.seek(-2, os.SEEK_CUR)
        bytes_written = self.f.write(struct.pack(self.longFmt, value))
        if bytes_written is not None and bytes_written != 4:
            msg = f"wrote only {bytes_written} bytes but wanted 4"
            raise RuntimeError(msg)
