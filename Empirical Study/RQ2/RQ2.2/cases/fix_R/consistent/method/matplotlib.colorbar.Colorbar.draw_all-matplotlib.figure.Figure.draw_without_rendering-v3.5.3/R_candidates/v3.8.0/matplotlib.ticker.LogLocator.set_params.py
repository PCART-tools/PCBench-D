    @_api.delete_parameter("3.8", "numdecs")
    def set_params(self, base=None, subs=None, numdecs=None, numticks=None):
        """Set parameters within this locator."""
        if base is not None:
            self._base = float(base)
        if subs is not None:
            self._set_subs(subs)
        if numdecs is not None:
            self._numdecs = numdecs
        if numticks is not None:
            self.numticks = numticks
