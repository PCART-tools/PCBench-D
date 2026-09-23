    def close(self) -> None:
        """
        Close transport and proxies.
        """
        self._transport.close()
        for proxy in self._proxies.values():
            if proxy is not None:
                proxy.close()
