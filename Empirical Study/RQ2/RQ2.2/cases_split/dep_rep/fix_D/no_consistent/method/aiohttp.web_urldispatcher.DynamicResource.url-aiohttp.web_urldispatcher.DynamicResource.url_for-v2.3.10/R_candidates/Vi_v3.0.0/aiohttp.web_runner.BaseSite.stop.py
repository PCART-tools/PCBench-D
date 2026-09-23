    async def stop(self):
        self._runner._check_site(self)
        if self._server is None:
            self._runner._unreg_site(self)
            return  # not started yet
        self._server.close()
        await self._server.wait_closed()
        await self._runner.shutdown()
        await self._runner.server.shutdown(self._shutdown_timeout)
        self._runner._unreg_site(self)
