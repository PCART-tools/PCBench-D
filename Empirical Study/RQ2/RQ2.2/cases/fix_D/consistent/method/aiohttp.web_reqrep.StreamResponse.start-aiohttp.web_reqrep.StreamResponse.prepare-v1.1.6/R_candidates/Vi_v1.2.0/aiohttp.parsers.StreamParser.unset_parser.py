    def unset_parser(self):
        """unset parser, send eof to the parser and then remove it."""
        if self._parser is None:
            return

        # TODO: write test
        if self._loop.is_closed():
            # TODO: log something
            return

        try:
            self._parser.throw(EofStream())
        except StopIteration:
            self._output.feed_eof()
        except EofStream:
            self._output.set_exception(self._eof_exc_class())
        except Exception as exc:
            self._output.set_exception(exc)
        finally:
            self._output = None
            self._parser = None
