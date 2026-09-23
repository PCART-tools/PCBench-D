    async def send_dns_cache_miss(self, host):
        return await self._trace_config.on_dns_cache_miss.send(
            self._session,
            self._trace_config_ctx,
            TraceDnsCacheMissParams(host)
        )
