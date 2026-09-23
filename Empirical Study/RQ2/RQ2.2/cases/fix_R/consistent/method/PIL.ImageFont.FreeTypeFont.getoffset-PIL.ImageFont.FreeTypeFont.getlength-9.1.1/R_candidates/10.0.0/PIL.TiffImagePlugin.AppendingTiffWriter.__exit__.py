    def __exit__(self, exc_type, exc_value, traceback):
        if self.close_fp:
            self.close()
        return False
