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
        raise AbstractMethodError(self)
