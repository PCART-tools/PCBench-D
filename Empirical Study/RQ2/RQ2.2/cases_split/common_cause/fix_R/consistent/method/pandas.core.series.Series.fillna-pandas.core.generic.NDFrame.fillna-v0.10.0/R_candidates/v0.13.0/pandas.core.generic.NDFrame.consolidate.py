    def consolidate(self, inplace=False):
        """
        Compute NDFrame with "consolidated" internals (data of each dtype
        grouped together in a single ndarray). Mainly an internal API function,
        but available here to the savvy user

        Parameters
        ----------
        inplace : boolean, default False
            If False return new object, otherwise modify existing object

        Returns
        -------
        consolidated : type of caller
        """
        if inplace:
            self._consolidate_inplace()
        else:
            f = lambda: self._data.consolidate()
            cons_data = self._protect_consolidate(f)
            if cons_data is self._data:
                cons_data = cons_data.copy()
            return self._constructor(cons_data).__finalize__(self)
