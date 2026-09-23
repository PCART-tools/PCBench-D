    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def shift(self, periods=1, freq=None, axis=0, fill_value=None):
        """
        Shift each group by periods observations.

        Parameters
        ----------
        periods : int, default 1
            Number of periods to shift.
        freq : frequency string
        axis : axis to shift, default 0
        fill_value : optional

            .. versionadded:: 0.24.0

        Returns
        -------
        Series or DataFrame
            Object shifted within each group.
        """

        if freq is not None or axis != 0 or not isna(fill_value):
            return self.apply(lambda x: x.shift(periods, freq, axis, fill_value))

        return self._get_cythonized_result(
            "group_shift_indexer",
            cython_dtype=np.dtype(np.int64),
            needs_ngroups=True,
            result_is_index=True,
            periods=periods,
        )
