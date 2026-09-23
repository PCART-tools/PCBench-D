    @deprecate_kwarg(old_arg_name="numeric_only", new_arg_name="skipna")
    def max(self, skipna=True, **kwargs):
        """
        The maximum value of the object.

        Only ordered `Categoricals` have a maximum!

        .. versionchanged:: 1.0.0

           Returns an NA value on empty arrays

        Raises
        ------
        TypeError
            If the `Categorical` is not `ordered`.

        Returns
        -------
        max : the maximum of this `Categorical`
        """
        nv.validate_max((), kwargs)
        self.check_for_ordered("max")

        if not len(self._codes):
            return self.dtype.na_value

        good = self._codes != -1
        if not good.all():
            if skipna and good.any():
                pointer = self._codes[good].max()
            else:
                return np.nan
        else:
            pointer = self._codes.max()
        return self.categories[pointer]
