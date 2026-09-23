    async def close(self, *, code=1000, message=b''):
        # we need to break `receive()` cycle first,
        # `close()` may be called from different task
        if self._waiting is not None and not self._closed:
            self._reader.feed_data(WS_CLOSING_MESSAGE, 0)
            await self._waiting

        if not self._closed:
            self._cancel_heartbeat()
            self._closed = True
            try:
                self._writer.close(code, message)
            except asyncio.CancelledError:
                self._close_code = 1006
                self._response.close()
                raise
            except Exception as exc:
                self._close_code = 1006
                self._exception = exc
                self._response.close()
                return True

            if self._closing:
                self._response.close()
                return True

            while True:
                try:
                    with async_timeout.timeout(self._timeout, loop=self._loop):
                        msg = await self._reader.read()
                except asyncio.CancelledError:
                    self._close_code = 1006
                    self._response.close()
                    raise
                except Exception as exc:
                    self._close_code = 1006
                    self._exception = exc
                    self._response.close()
                    return True

                if msg.type == WSMsgType.CLOSE:
                    self._close_code = msg.data
                    self._response.close()
                    return True
        else:
            return False
