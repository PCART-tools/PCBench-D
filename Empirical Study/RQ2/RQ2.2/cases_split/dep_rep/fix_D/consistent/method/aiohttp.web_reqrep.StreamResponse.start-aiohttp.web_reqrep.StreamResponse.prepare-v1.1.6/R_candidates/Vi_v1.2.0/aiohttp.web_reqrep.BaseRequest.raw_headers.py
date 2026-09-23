    @reify
    def raw_headers(self):
        """A sequence of pars for all headers."""
        return tuple(self._message.raw_headers)
