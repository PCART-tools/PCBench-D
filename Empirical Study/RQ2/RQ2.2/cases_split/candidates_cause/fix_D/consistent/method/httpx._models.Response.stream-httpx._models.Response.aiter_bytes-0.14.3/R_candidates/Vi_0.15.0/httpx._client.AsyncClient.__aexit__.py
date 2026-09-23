    async def __aexit__(
        self,
        exc_type: typing.Type[BaseException] = None,
        exc_value: BaseException = None,
        traceback: TracebackType = None,
    ) -> None:
        if not self.is_closed:
            self._is_closed = True
            await self._transport.__aexit__(exc_type, exc_value, traceback)
            for proxy in self._proxies.values():
                if proxy is not None:
                    await proxy.__aexit__(exc_type, exc_value, traceback)
