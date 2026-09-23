    def set_exception(self, exc):
        if isinstance(exc, ConnectionError):
            exc, old_exc = self._eof_exc_class(), exc
            exc.__cause__ = old_exc
            exc.__context__ = old_exc

        self._exception = exc

        if self._output is not None:
            self._output.set_exception(exc)
            self._output = None
            self._parser = None
