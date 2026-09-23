    async def send_connection_create_end(self):
        return await self._trace_config.on_connection_create_end.send(
            self._session,
            self._trace_config_ctx,
            TraceConnectionCreateEndParams()
        )
