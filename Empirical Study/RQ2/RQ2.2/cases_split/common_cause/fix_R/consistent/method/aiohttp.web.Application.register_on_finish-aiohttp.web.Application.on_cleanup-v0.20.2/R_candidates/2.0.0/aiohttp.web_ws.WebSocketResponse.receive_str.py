    @asyncio.coroutine
    def receive_str(self, *, timeout=None):
        msg = yield from self.receive(timeout)
        if msg.type != WSMsgType.TEXT:
            raise TypeError(
                "Received message {}:{!r} is not WSMsgType.TEXT".format(
                    msg.type, msg.data))
        return msg.data
