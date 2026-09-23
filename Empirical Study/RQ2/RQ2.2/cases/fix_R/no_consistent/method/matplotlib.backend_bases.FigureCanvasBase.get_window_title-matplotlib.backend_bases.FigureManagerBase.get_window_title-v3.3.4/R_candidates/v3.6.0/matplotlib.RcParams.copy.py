    def copy(self):
        """Copy this RcParams instance."""
        rccopy = RcParams()
        for k in self:  # Skip deprecations and revalidation.
            dict.__setitem__(rccopy, k, dict.__getitem__(self, k))
        return rccopy
