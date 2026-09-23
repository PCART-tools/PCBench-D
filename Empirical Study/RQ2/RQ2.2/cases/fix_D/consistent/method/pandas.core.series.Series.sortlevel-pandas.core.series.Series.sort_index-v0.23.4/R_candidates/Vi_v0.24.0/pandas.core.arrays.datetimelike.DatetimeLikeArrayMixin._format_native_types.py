    def _format_native_types(self, na_rep='NaT', date_format=None):
        """
        Helper method for astype when converting to strings.

        Returns
        -------
        ndarray[str]
        """
        raise AbstractMethodError(self)
