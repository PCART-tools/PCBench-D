    async def send_dns_resolvehost_start(self, host):
        return await self._trace_config.on_dns_resolvehost_start.send(
            self._session,
            self._trace_config_ctx,
            TraceDnsResolveHostStartParams(host)
        )
