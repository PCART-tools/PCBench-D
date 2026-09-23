    @asyncio.coroutine
    def receive_bytes(self):
        msg = yield from self.receive()
        if msg.type != WSMsgType.BINARY:
            raise TypeError(
                "Received message {}:{!r} is not bytes".format(msg.type,
                                                               msg.data))
        return msg.data
