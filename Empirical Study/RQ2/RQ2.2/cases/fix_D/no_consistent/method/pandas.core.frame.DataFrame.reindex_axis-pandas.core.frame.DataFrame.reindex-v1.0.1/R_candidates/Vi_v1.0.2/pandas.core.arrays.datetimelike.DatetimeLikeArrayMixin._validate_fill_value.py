    def _validate_fill_value(self, fill_value):
        """
        If a fill_value is passed to `take` convert it to an i8 representation,
        raising ValueError if this is not possible.

        Parameters
        ----------
        fill_value : object

        Returns
        -------
        fill_value : np.int64

        Raises
        ------
        ValueError
        """
        if isna(fill_value):
            fill_value = iNaT
        elif isinstance(fill_value, self._recognized_scalars):
            self._check_compatible_with(fill_value)
            fill_value = self._scalar_type(fill_value)
            fill_value = self._unbox_scalar(fill_value)
        else:
            raise ValueError(
                f"'fill_value' should be a {self._scalar_type}. Got '{fill_value}'."
            )
        return fill_value
