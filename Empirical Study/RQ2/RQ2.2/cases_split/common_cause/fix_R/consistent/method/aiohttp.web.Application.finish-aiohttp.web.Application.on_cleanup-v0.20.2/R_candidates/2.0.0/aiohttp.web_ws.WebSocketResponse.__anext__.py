        @asyncio.coroutine
        def __anext__(self):
            msg = yield from self.receive()
            if msg.type in (WSMsgType.CLOSE,
                            WSMsgType.CLOSING,
                            WSMsgType.CLOSED):
                raise StopAsyncIteration  # NOQA
            return msg
