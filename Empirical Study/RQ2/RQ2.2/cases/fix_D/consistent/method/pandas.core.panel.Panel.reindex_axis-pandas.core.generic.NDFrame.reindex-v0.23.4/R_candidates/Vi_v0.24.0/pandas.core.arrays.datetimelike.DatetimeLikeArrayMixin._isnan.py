    @property  # NB: override with cache_readonly in immutable subclasses
    def _isnan(self):
        """
        return if each value is nan
        """
        return (self.asi8 == iNaT)
