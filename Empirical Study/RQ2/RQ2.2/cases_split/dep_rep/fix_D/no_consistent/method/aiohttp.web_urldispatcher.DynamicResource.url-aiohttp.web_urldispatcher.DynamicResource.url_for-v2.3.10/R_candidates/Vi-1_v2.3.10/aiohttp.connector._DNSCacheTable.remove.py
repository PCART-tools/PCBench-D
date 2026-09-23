    def remove(self, host):
        self._addrs.pop(host, None)
        self._addrs_rr.pop(host, None)

        if self._ttl:
            self._timestamps.pop(host, None)
