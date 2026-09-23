    async def _cleanup_server(self):
        await self._app.cleanup()
