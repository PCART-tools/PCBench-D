    def available(self, o):
        """Return whether drawing is available to *o*."""
        return not self.locked() or self.isowner(o)
