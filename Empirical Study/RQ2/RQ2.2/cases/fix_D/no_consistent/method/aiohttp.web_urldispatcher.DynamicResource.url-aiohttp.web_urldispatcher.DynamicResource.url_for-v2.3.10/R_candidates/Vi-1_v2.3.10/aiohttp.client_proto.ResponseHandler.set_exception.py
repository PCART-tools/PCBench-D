    def set_exception(self, exc):
        self._should_close = True

        super().set_exception(exc)
