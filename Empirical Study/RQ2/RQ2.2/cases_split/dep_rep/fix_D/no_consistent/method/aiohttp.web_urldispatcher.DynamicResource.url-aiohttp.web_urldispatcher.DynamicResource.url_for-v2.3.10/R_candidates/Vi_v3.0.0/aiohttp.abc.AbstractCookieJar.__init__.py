    def __init__(self, *, loop=None):
        self._loop = loop or asyncio.get_event_loop()
