    def add(self, host, addrs):
        self._addrs_rr[host] = (cycle(addrs), len(addrs))

        if self._ttl:
            self._timestamps[host] = monotonic()
