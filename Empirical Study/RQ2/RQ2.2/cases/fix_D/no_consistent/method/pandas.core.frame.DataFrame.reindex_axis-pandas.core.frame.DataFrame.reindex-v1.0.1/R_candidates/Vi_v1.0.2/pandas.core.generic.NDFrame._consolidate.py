    def _consolidate(self, inplace: bool_t = False):
        """
        Compute NDFrame with "consolidated" internals (data of each dtype
        grouped together in a single ndarray).

        Parameters
        ----------
        inplace : bool, default False
            If False return new object, otherwise modify existing object.

        Returns
        -------
        consolidated : same type as caller
        """
        inplace = validate_bool_kwarg(inplace, "inplace")
        if inplace:
            self._consolidate_inplace()
        else:
            f = lambda: self._data.consolidate()
            cons_data = self._protect_consolidate(f)
            return self._constructor(cons_data).__finalize__(self)
