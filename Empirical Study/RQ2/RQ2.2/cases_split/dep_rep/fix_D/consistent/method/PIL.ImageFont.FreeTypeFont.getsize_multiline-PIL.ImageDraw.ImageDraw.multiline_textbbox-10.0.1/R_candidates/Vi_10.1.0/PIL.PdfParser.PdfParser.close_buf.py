    def close_buf(self):
        try:
            self.buf.close()
        except AttributeError:
            pass
        self.buf = None
