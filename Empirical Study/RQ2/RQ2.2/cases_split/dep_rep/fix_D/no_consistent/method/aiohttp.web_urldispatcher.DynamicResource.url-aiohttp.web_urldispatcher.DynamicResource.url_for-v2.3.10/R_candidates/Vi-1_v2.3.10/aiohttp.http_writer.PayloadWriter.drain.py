    @asyncio.coroutine
    def drain(self, last=False):
        if self._transport is not None:
            if self._buffer:
                self._transport.write(b''.join(self._buffer))
                if not last:
                    self._buffer.clear()
            yield from self._stream.drain()
        else:
            # wait for transport
            if self._drain_waiter is None:
                self._drain_waiter = create_future(self.loop)

            yield from self._drain_waiter
