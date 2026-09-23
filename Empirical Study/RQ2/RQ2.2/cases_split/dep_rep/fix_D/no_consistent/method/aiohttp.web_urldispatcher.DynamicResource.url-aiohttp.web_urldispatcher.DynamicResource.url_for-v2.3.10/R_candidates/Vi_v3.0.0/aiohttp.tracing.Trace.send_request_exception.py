    async def send_request_exception(self, method, url, headers, exception):
        return await self._trace_config.on_request_exception.send(
            self._session,
            self._trace_config_ctx,
            TraceRequestExceptionParams(method, url, headers, exception)
        )
