    def __exit__(
        self,
        exc_type: typing.Type[BaseException] = None,
        exc_value: BaseException = None,
        traceback: TracebackType = None,
    ) -> None:
        self._transport.__exit__(exc_type, exc_value, traceback)
        for proxy in self._proxies.values():
            if proxy is not None:
                proxy.__exit__(exc_type, exc_value, traceback)
