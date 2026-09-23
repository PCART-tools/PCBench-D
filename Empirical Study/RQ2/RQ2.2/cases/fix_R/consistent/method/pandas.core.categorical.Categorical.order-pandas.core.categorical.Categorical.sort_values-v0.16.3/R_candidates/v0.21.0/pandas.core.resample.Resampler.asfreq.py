    def asfreq(self, fill_value=None):
        """
        return the values at the new freq,
        essentially a reindex

        Parameters
        ----------
        fill_value: scalar, optional
            Value to use for missing values, applied during upsampling (note
            this does not fill NaNs that already were present).

            .. versionadded:: 0.20.0

        See Also
        --------
        Series.asfreq
        DataFrame.asfreq
        """
        return self._upsample('asfreq', fill_value=fill_value)
