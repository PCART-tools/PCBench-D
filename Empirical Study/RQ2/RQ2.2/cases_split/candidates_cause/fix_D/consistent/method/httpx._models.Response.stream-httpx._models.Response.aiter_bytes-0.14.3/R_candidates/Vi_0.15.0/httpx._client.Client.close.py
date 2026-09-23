    def close(self) -> None:
        """
        Close transport and proxies.
        """
        if not self.is_closed:
            self._is_closed = True

            self._transport.close()
            for proxy in self._proxies.values():
                if proxy is not None:
                    proxy.close()
