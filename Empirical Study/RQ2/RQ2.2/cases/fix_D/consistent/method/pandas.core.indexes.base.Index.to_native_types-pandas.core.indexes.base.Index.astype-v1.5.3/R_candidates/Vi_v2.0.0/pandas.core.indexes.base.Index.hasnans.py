    @cache_readonly
    def hasnans(self) -> bool:
        """
        Return True if there are any NaNs.

        Enables various performance speedups.

        Returns
        -------
        bool
        """
        if self._can_hold_na:
            return bool(self._isnan.any())
        else:
            return False
