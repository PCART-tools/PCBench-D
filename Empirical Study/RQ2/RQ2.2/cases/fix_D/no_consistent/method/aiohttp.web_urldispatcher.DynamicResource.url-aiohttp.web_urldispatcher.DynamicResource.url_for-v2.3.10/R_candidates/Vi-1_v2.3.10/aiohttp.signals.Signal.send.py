    @asyncio.coroutine
    def send(self, *args, **kwargs):
        """
        Sends data to all registered receivers.
        """
        if self:
            ordinal = None
            debug = self._app._debug
            if debug:
                ordinal = self._pre.ordinal()
                yield from self._pre.send(
                    ordinal, self._name, *args, **kwargs)
            yield from self._send(*args, **kwargs)
            if debug:
                yield from self._post.send(
                    ordinal, self._name, *args, **kwargs)
