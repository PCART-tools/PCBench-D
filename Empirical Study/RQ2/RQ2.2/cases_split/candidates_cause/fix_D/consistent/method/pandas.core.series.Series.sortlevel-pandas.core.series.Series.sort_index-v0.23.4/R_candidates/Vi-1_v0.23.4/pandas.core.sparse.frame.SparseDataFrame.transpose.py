    def transpose(self, *args, **kwargs):
        """
        Returns a DataFrame with the rows/columns switched.
        """
        nv.validate_transpose(args, kwargs)
        return self._constructor(
            self.values.T, index=self.columns, columns=self.index,
            default_fill_value=self._default_fill_value,
            default_kind=self._default_kind).__finalize__(self)
