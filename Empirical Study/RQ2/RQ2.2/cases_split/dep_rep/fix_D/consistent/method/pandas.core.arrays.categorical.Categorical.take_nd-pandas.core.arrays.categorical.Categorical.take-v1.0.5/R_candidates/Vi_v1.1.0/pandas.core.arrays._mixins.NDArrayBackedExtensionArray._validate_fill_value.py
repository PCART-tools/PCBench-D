    def _validate_fill_value(self, fill_value):
        """
        If a fill_value is passed to `take` convert it to a representation
        suitable for self._ndarray, raising ValueError if this is not possible.

        Parameters
        ----------
        fill_value : object

        Returns
        -------
        fill_value : native representation

        Raises
        ------
        ValueError
        """
        raise AbstractMethodError(self)
