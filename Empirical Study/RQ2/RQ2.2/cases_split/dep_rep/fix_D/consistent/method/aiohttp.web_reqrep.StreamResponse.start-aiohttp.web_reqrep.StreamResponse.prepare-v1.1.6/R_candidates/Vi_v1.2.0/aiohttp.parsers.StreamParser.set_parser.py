    def set_parser(self, parser, output=None):
        """set parser to stream. return parser's DataQueue."""
        if self._parser:
            self.unset_parser()

        if output is None:
            output = FlowControlDataQueue(
                self, limit=self._limit, loop=self._loop)

        if self._exception:
            output.set_exception(self._exception)
            return output

        # init parser
        p = parser(output, self._buffer)

        try:
            # initialize parser with data and parser buffers
            next(p)
        except StopIteration:
            pass
        except Exception as exc:
            output.set_exception(exc)
        else:
            # parser still require more data
            self._parser = p
            self._output = output

            if self._eof:
                self.unset_parser()

        return output
