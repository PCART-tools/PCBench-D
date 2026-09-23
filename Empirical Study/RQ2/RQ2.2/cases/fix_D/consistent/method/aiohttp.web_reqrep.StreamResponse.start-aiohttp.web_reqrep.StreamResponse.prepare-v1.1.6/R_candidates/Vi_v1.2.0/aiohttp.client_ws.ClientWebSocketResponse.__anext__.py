        @asyncio.coroutine
        def __anext__(self):
            msg = yield from self.receive()
            if msg.type == WSMsgType.CLOSE or msg.type == WSMsgType.CLOSED:
                raise StopAsyncIteration  # NOQA
            return msg
