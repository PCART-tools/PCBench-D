    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False  # do not suppress exceptions
