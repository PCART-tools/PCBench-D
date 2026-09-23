    def clear(self):
        self._cookies.clear()
        self._host_only_cookies.clear()
        self._next_expiration = ceil(self._loop.time())
        self._expirations.clear()
