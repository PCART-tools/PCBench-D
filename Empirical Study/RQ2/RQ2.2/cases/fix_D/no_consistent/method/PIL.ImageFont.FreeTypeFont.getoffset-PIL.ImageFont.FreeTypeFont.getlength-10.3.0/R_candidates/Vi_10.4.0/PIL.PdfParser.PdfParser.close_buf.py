    def close_buf(self) -> None:
        try:
            self.buf.close()
        except AttributeError:
            pass
        self.buf = None
