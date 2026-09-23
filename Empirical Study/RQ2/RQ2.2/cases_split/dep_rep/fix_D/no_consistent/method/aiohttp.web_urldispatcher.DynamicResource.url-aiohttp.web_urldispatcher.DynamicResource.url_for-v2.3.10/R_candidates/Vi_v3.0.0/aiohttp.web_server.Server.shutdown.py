    async def shutdown(self, timeout=None):
        coros = [conn.shutdown(timeout) for conn in self._connections]
        await asyncio.gather(*coros, loop=self._loop)
        self._connections.clear()
