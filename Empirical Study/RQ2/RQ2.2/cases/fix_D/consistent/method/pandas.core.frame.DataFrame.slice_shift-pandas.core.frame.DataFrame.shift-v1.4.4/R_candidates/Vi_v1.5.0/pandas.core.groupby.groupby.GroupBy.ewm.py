    @final
    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def ewm(self, *args, **kwargs) -> ExponentialMovingWindowGroupby:
        """
        Return an ewm grouper, providing ewm functionality per group.
        """
        from pandas.core.window import ExponentialMovingWindowGroupby

        return ExponentialMovingWindowGroupby(
            self._selected_obj,
            *args,
            _grouper=self.grouper,
            **kwargs,
        )
