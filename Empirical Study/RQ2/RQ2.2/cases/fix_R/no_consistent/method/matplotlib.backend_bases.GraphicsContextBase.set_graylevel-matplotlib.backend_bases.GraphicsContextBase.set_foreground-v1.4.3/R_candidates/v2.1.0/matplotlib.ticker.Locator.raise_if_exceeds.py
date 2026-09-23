    def raise_if_exceeds(self, locs):
        """raise a RuntimeError if Locator attempts to create more than
           MAXTICKS locs"""
        if len(locs) >= self.MAXTICKS:
            msg = ('Locator attempting to generate %d ticks from %s to %s: ' +
                   'exceeds Locator.MAXTICKS') % (len(locs), locs[0], locs[-1])
            raise RuntimeError(msg)

        return locs
