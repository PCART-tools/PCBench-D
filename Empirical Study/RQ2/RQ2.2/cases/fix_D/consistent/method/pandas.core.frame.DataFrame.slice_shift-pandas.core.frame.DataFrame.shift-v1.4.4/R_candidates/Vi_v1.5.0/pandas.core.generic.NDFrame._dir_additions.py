    @final
    def _dir_additions(self) -> set[str]:
        """
        add the string-like attributes from the info_axis.
        If info_axis is a MultiIndex, its first level values are used.
        """
        additions = super()._dir_additions()
        if self._info_axis._can_hold_strings:
            additions.update(self._info_axis._dir_additions_for_owner)
        return additions
