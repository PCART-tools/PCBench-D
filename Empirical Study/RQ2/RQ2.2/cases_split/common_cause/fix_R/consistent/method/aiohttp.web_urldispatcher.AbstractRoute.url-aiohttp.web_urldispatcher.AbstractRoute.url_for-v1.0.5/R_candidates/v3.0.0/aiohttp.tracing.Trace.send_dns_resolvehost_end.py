    async def send_dns_resolvehost_end(self, host):
        return await self._trace_config.on_dns_resolvehost_end.send(
            self._session,
            self._trace_config_ctx,
            TraceDnsResolveHostEndParams(host)
        )
