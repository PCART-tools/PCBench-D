    @final
    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def rolling(self, *args, **kwargs):
        """
        Return a rolling grouper, providing rolling functionality per group.
        """
        from pandas.core.window import RollingGroupby

        return RollingGroupby(
            self._selected_obj,
            *args,
            _grouper=self.grouper,
            _as_index=self.as_index,
            **kwargs,
        )
