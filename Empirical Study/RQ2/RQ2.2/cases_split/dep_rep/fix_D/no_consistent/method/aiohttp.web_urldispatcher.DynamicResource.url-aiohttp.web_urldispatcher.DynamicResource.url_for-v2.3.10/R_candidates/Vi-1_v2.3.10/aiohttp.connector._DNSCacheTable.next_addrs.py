    def next_addrs(self, host):
        loop = self._addrs_rr[host]
        addrs = list(islice(loop, len(self._addrs[host])))
        # Consume one more element to shift internal state of `cycle`
        next(loop)
        return addrs
