    @property  # NB: override with cache_readonly in immutable subclasses
    def _isnan(self) -> npt.NDArray[np.bool_]:
        """
        return if each value is nan
        """
        return self.asi8 == iNaT
