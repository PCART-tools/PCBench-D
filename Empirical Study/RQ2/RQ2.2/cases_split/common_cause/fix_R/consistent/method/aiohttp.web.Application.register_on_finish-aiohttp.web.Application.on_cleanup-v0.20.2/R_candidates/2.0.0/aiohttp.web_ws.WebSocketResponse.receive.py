    @asyncio.coroutine
    def receive(self, timeout=None):
        if self._reader is None:
            raise RuntimeError('Call .prepare() first')

        while True:
            if self._waiting is not None:
                raise RuntimeError(
                    'Concurrent call to receive() is not allowed')

            if self._closed:
                self._conn_lost += 1
                if self._conn_lost >= THRESHOLD_CONNLOST_ACCESS:
                    raise RuntimeError('WebSocket connection is closed.')
                return WS_CLOSED_MESSAGE
            elif self._closing:
                return WS_CLOSING_MESSAGE

            try:
                self._waiting = create_future(self._loop)
                try:
                    with Timeout(
                            timeout or self._receive_timeout, loop=self._loop):
                        msg = yield from self._reader.read()
                finally:
                    self._reset_heartbeat()
                    waiter = self._waiting
                    self._waiting = None
                    waiter.set_result(True)
            except (asyncio.CancelledError, asyncio.TimeoutError) as exc:
                self._close_code = 1006
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
            elif msg.type == WSMsgType.CLOSING:
                self._closing = True
            elif msg.type == WSMsgType.PING and self._autoping:
                self.pong(msg.data)
                continue
            elif msg.type == WSMsgType.PONG and self._autoping:
                continue

            return msg
