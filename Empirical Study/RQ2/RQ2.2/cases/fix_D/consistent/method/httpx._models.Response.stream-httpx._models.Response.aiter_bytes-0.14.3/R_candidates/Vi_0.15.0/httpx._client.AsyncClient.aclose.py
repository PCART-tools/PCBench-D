    async def aclose(self) -> None:
        """
        Close transport and proxies.
        """
        if not self.is_closed:
            self._is_closed = True

            await self._transport.aclose()
            for proxy in self._proxies.values():
                if proxy is not None:
                    await proxy.aclose()
