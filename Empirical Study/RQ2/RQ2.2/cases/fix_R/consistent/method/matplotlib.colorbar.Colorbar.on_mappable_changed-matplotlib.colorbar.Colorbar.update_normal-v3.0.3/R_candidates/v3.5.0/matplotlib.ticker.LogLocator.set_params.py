    def set_params(self, base=None, subs=None, numdecs=None, numticks=None):
        """Set parameters within this locator."""
        if base is not None:
            self.base(base)
        if subs is not None:
            self.subs(subs)
        if numdecs is not None:
            self.numdecs = numdecs
        if numticks is not None:
            self.numticks = numticks
