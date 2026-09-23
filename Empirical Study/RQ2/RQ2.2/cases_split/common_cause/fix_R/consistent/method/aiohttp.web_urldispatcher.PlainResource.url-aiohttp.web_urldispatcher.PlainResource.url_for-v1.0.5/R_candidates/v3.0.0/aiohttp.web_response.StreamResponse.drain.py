    async def drain(self):
        assert not self._eof_sent, "EOF has already been sent"
        assert self._payload_writer is not None, \
            "Response has not been started"
        warnings.warn("drain method is deprecated, use await resp.write()",
                      DeprecationWarning,
                      stacklevel=2)
        await self._payload_writer.drain()
