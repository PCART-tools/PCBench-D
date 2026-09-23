    def _drop_acquired_per_host(self, key, val):
        acquired_per_host = self._acquired_per_host
        if key not in acquired_per_host:
            return
        conns = acquired_per_host[key]
        conns.remove(val)
        if not conns:
            del self._acquired_per_host[key]
