    async def send_request_redirect(self, method, url, headers, response):
        return await self._trace_config._on_request_redirect.send(
            self._session,
            self._trace_config_ctx,
            TraceRequestRedirectParams(method, url, headers, response)
        )
