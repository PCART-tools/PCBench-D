    async def __anext__(self):
        msg = await self.receive()
        if msg.type in (WSMsgType.CLOSE,
                        WSMsgType.CLOSING,
                        WSMsgType.CLOSED):
            raise StopAsyncIteration  # NOQA
        return msg
