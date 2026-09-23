    @asyncio.coroutine
    def close(self, *, code=1000, message=b''):
        if not self._closed:
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
                    msg = yield from asyncio.wait_for(
                        self._reader.read(), self._timeout, loop=self._loop)
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
