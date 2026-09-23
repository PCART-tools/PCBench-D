    def next_addrs(self, host):
        loop, length = self._addrs_rr[host]
        addrs = list(islice(loop, length))
        # Consume one more element to shift internal state of `cycle`
        next(loop)
        return addrs
