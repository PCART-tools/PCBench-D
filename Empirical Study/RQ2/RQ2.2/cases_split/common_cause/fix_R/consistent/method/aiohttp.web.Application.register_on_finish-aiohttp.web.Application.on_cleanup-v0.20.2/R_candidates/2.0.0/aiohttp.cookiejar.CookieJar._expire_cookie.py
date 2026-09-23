    def _expire_cookie(self, when, domain, name):
        self._next_expiration = min(self._next_expiration, when)
        self._expirations[(domain, name)] = when
