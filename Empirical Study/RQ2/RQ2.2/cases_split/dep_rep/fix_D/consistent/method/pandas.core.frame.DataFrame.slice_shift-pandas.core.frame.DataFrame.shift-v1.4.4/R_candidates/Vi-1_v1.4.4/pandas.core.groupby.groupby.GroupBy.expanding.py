    @final
    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def expanding(self, *args, **kwargs):
        """
        Return an expanding grouper, providing expanding
        functionality per group.
        """
        from pandas.core.window import ExpandingGroupby

        return ExpandingGroupby(
            self._selected_obj,
            *args,
            _grouper=self.grouper,
            **kwargs,
        )
