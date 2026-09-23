    def feed_eof(self):
        """send eof to all parsers, recursively."""
        if self._parser:
            try:
                if self._buffer:
                    self._parser.send(b'')
                self._parser.throw(EofStream())
            except StopIteration:
                self._output.feed_eof()
            except EofStream:
                self._output.set_exception(self._eof_exc_class())
            except Exception as exc:
                self._output.set_exception(exc)

            self._parser = None
            self._output = None

        self._eof = True
