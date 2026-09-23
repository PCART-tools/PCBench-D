    @asyncio.coroutine
    def close(self, *, code=1000, message=b''):
        if self._writer is None:
            raise RuntimeError('Call .prepare() first')

        if not self._closed:
            self._closed = True
            try:
                self._writer.close(code, message)
            except (asyncio.CancelledError, asyncio.TimeoutError):
                self._close_code = 1006
                raise
            except Exception as exc:
                self._close_code = 1006
                self._exception = exc
                return True

            if self._closing:
                return True

            begin = self._loop.time()
            while self._loop.time() - begin < self._timeout:
                try:
                    with Timeout(timeout=self._timeout,
                                 loop=self._loop):
                        msg = yield from self._reader.read()
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
