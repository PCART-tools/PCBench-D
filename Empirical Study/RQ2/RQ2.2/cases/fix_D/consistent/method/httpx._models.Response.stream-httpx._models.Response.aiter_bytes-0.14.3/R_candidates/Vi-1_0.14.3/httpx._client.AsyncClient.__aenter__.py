    async def __aenter__(self) -> "AsyncClient":
        await self._transport.__aenter__()
        for proxy in self._proxies.values():
            if proxy is not None:
                await proxy.__aenter__()
        return self
