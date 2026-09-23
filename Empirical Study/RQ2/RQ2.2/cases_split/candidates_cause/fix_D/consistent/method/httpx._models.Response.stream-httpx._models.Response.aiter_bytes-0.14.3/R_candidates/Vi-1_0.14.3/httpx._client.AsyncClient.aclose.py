    async def aclose(self) -> None:
        """
        Close transport and proxies.
        """
        await self._transport.aclose()
        for proxy in self._proxies.values():
            if proxy is not None:
                await proxy.aclose()
