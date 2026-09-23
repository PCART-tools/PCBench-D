    def set_names(self, names, inplace=False):
        """
        Set new names on index. Defaults to returning new index.

        Parameters
        ----------
        names : sequence
            names to set
        inplace : bool
            if True, mutates in place

        Returns
        -------
        new index (of same type and class...etc) [if inplace, returns None]
        """
        if not com.is_list_like(names):
            raise TypeError("Must pass list-like as `names`.")
        if inplace:
            idx = self
        else:
            idx = self._shallow_copy()
        idx._set_names(names)
        if not inplace:
            return idx
