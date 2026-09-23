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
        msg = (
            f"'fill_value' should be a {self._scalar_type}. "
            f"Got '{str(fill_value)}'."
        )
        try:
            fill_value = self._validate_scalar(fill_value, msg)
        except TypeError as err:
            raise ValueError(msg) from err
        return self._unbox(fill_value)
