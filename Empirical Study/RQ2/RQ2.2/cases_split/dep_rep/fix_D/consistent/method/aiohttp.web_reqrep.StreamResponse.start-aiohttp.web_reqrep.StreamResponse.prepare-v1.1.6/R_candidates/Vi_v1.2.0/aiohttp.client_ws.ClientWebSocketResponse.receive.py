    @asyncio.coroutine
    def receive(self):
        if self._waiting:
            raise RuntimeError('Concurrent call to receive() is not allowed')

        self._waiting = True
        try:
            while True:
                if self._closed:
                    return CLOSED_MESSAGE

                try:
                    msg = yield from self._reader.read()
                except (asyncio.CancelledError, asyncio.TimeoutError):
                    raise
                except WebSocketError as exc:
                    self._close_code = exc.code
                    yield from self.close(code=exc.code)
                    return WSMessage(WSMsgType.ERROR, exc, None)
                except Exception as exc:
                    self._exception = exc
                    self._closing = True
                    self._close_code = 1006
                    yield from self.close()
                    return WSMessage(WSMsgType.ERROR, exc, None)

                if msg.type == WSMsgType.CLOSE:
                    self._closing = True
                    self._close_code = msg.data
                    if not self._closed and self._autoclose:
                        yield from self.close()
                    return msg
                if msg.type == WSMsgType.PING and self._autoping:
                    self.pong(msg.data)
                elif msg.type == WSMsgType.PONG and self._autoping:
                    continue
                else:
                    return msg
        finally:
            self._waiting = False
