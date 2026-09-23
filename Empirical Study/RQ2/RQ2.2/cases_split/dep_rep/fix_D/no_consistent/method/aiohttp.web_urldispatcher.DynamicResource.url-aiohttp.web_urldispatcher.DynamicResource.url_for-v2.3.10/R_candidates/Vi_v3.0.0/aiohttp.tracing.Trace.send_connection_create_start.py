    async def send_connection_create_start(self):
        return await self._trace_config.on_connection_create_start.send(
            self._session,
            self._trace_config_ctx,
            TraceConnectionCreateStartParams()
        )
