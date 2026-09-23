    @deprecate_kwarg(old_arg_name="numeric_only", new_arg_name="skipna")
    def min(self, skipna=True):
        """
        The minimum value of the object.

        Only ordered `Categoricals` have a minimum!

        .. versionchanged:: 1.0.0

           Returns an NA value on empty arrays

        Raises
        ------
        TypeError
            If the `Categorical` is not `ordered`.

        Returns
        -------
        min : the minimum of this `Categorical`
        """
        self.check_for_ordered("min")

        if not len(self._codes):
            return self.dtype.na_value

        good = self._codes != -1
        if not good.all():
            if skipna:
                pointer = self._codes[good].min()
            else:
                return np.nan
        else:
            pointer = self._codes.min()
        return self.categories[pointer]
