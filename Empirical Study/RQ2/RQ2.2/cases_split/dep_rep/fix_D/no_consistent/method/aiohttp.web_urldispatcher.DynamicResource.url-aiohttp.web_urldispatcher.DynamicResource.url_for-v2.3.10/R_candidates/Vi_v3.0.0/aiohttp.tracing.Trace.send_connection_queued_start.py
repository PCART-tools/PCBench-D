    async def send_connection_queued_start(self):
        return await self._trace_config.on_connection_queued_start.send(
            self._session,
            self._trace_config_ctx,
            TraceConnectionQueuedStartParams()
        )
