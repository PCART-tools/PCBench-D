    async def write(self, data):
        raise RuntimeError("Cannot call .write() for websocket")
