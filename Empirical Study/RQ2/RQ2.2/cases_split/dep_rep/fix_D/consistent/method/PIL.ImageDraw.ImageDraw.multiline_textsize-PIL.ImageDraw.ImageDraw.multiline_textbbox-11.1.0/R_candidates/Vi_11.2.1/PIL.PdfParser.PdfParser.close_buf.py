    def close_buf(self) -> None:
        if isinstance(self.buf, mmap.mmap):
            self.buf.close()
        self.buf = None
