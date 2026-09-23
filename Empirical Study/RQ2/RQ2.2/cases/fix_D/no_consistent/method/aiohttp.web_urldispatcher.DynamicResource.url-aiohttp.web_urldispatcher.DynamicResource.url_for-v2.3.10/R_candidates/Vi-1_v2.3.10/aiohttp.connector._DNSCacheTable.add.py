    def add(self, host, addrs):
        self._addrs[host] = addrs
        self._addrs_rr[host] = cycle(addrs)

        if self._ttl:
            self._timestamps[host] = monotonic()
