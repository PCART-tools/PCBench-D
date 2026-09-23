    def raise_if_exceeds(self, locs):
        """raise a RuntimeError if Locator attempts to create more than
           MAXTICKS locs"""
        if len(locs) >= self.MAXTICKS:
            raise RuntimeError("Locator attempting to generate {} ticks from "
                               "{} to {}: exceeds Locator.MAXTICKS".format(
                                   len(locs), locs[0], locs[-1]))
        return locs
