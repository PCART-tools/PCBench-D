    def _do_expiration(self):
        now = self._loop.time()
        if self._next_expiration > now:
            return
        if not self._expirations:
            return
        next_expiration = self.MAX_TIME
        to_del = []
        cookies = self._cookies
        expirations = self._expirations
        for (domain, name), when in expirations.items():
            if when < now:
                cookies[domain].pop(name, None)
                to_del.append((domain, name))
                self._host_only_cookies.discard((domain, name))
            else:
                next_expiration = min(next_expiration, when)
        for key in to_del:
            del expirations[key]

        self._next_expiration = ceil(next_expiration)
