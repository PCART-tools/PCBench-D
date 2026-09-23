    async def send_connection_reuseconn(self):
        return await self._trace_config.on_connection_reuseconn.send(
            self._session,
            self._trace_config_ctx,
            TraceConnectionReuseconnParams()
        )
