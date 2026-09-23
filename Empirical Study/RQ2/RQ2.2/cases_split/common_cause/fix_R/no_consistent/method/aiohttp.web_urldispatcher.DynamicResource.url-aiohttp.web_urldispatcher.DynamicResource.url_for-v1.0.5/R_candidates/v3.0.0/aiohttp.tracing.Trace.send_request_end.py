    async def send_request_end(self, method, url, headers, response):
        return await self._trace_config.on_request_end.send(
            self._session,
            self._trace_config_ctx,
            TraceRequestEndParams(method, url, headers, response)
        )
