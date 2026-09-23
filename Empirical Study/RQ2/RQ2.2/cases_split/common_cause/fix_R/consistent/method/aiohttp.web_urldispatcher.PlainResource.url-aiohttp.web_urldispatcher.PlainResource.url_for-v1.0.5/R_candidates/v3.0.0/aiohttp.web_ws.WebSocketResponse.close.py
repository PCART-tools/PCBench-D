    async def close(self, *, code=1000, message=b''):
        if self._writer is None:
            raise RuntimeError('Call .prepare() first')

        self._cancel_heartbeat()

        # we need to break `receive()` cycle first,
        # `close()` may be called from different task
        if self._waiting is not None and not self._closed:
            self._reader.feed_data(WS_CLOSING_MESSAGE, 0)
            await self._waiting

        if not self._closed:
            self._closed = True
            try:
                self._writer.close(code, message)
                await self._payload_writer.drain()
            except (asyncio.CancelledError, asyncio.TimeoutError):
                self._close_code = 1006
                raise
            except Exception as exc:
                self._close_code = 1006
                self._exception = exc
                return True

            if self._closing:
                return True

            try:
                with async_timeout.timeout(self._timeout, loop=self._loop):
                    msg = await self._reader.read()
            except asyncio.CancelledError:
                self._close_code = 1006
                raise
            except Exception as exc:
                self._close_code = 1006
                self._exception = exc
                return True

            if msg.type == WSMsgType.CLOSE:
                self._close_code = msg.data
                return True

            self._close_code = 1006
            self._exception = asyncio.TimeoutError()
            return True
        else:
            return False
