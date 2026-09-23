    def __exit__(
        self,
        exc_type: typing.Type[BaseException] = None,
        exc_value: BaseException = None,
        traceback: TracebackType = None,
    ) -> None:
        if not self.is_closed:
            self._is_closed = True

            self._transport.__exit__(exc_type, exc_value, traceback)
            for proxy in self._proxies.values():
                if proxy is not None:
                    proxy.__exit__(exc_type, exc_value, traceback)
