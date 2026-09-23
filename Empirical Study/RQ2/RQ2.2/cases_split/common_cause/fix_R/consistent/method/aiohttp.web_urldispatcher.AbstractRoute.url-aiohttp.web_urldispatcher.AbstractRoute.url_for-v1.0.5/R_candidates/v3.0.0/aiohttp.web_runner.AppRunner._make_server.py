    async def _make_server(self):
        loop = asyncio.get_event_loop()
        self._app._set_loop(loop)
        self._app.on_startup.freeze()
        await self._app.startup()
        self._app.freeze()

        return self._app.make_handler(loop=loop, **self._kwargs)
