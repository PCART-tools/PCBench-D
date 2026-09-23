    @dtl.ravel_compat
    def _format_native_types(
        self, *, na_rep="NaT", date_format=None, **kwargs
    ) -> np.ndarray:
        """
        actually format my specific types
        """
        values = self.astype(object)

        if date_format:
            formatter = lambda dt: dt.strftime(date_format)
        else:
            formatter = lambda dt: str(dt)

        if self._hasna:
            mask = self._isnan
            values[mask] = na_rep
            imask = ~mask
            values[imask] = np.array([formatter(dt) for dt in values[imask]])
        else:
            values = np.array([formatter(dt) for dt in values])
        return values
