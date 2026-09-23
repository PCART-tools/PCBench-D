    def __enter__(self) -> "Client":
        self._transport.__enter__()
        for proxy in self._proxies.values():
            if proxy is not None:
                proxy.__enter__()
        self._is_closed = False
        return self
