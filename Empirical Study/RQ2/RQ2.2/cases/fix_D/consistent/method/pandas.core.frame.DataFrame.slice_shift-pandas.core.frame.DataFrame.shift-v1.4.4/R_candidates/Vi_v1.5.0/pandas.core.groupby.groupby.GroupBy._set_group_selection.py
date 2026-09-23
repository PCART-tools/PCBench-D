    @final
    def _set_group_selection(self) -> None:
        """
        Create group based selection.

        Used when selection is not passed directly but instead via a grouper.

        NOTE: this should be paired with a call to _reset_group_selection
        """
        # This is a no-op for SeriesGroupBy
        grp = self.grouper
        if not (
            self.as_index
            and grp.groupings is not None
            and self.obj.ndim > 1
            and self._group_selection is None
        ):
            return

        groupers = [g.name for g in grp.groupings if g.level is None and g.in_axis]

        if len(groupers):
            # GH12839 clear selected obj cache when group selection changes
            ax = self.obj._info_axis
            self._group_selection = ax.difference(Index(groupers), sort=False).tolist()
            self._reset_cache("_selected_obj")
