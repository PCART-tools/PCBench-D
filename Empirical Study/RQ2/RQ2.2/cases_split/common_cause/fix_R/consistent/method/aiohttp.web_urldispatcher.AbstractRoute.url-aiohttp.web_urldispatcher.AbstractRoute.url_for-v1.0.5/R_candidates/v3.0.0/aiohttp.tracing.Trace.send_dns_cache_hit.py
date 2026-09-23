    async def send_dns_cache_hit(self, host):
        return await self._trace_config.on_dns_cache_hit.send(
            self._session,
            self._trace_config_ctx,
            TraceDnsCacheHitParams(host)
        )
