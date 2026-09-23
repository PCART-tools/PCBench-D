    def __enter__(self):
        self._loop.run_until_complete(self.start_server())
        return self
