    @asyncio.coroutine
    def receive_str(self):
        msg = yield from self.receive()
        if msg.type != WSMsgType.TEXT:
            raise TypeError(
                "Received message {}:{!r} is not str".format(msg.type,
                                                             msg.data))
        return msg.data
