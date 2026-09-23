    def __exit__(self, exc_type, exc_value, traceback):
        self._loop.run_until_complete(self.close())
