    def set_levels(self, levels, inplace=False, verify_integrity=True):
        """
        Set new levels on MultiIndex. Defaults to returning
        new index.

        Parameters
        ----------
        levels : sequence
            new levels to apply
        inplace : bool
            if True, mutates in place
        verify_integrity : bool (default True)
            if True, checks that levels and labels are compatible

        Returns
        -------
        new index (of same type and class...etc)
        """
        if not com.is_list_like(levels) or not com.is_list_like(levels[0]):
            raise TypeError("Levels must be list of lists-like")
        if inplace:
            idx = self
        else:
            idx = self._shallow_copy()
        idx._reset_identity()
        idx._set_levels(levels, validate=True,
                        verify_integrity=verify_integrity)
        if not inplace:
            return idx
