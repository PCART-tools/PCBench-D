    def _set_group_selection(self):
        """
        Create group based selection.

        Used when selection is not passed directly but instead via a grouper.

        NOTE: this should be paired with a call to _reset_group_selection
        """
        grp = self.grouper
        if not (
            self.as_index
            and getattr(grp, "groupings", None) is not None
            and self.obj.ndim > 1
            and self._group_selection is None
        ):
            return

        ax = self.obj._info_axis
        groupers = [g.name for g in grp.groupings if g.level is None and g.in_axis]

        if len(groupers):
            # GH12839 clear selected obj cache when group selection changes
            self._group_selection = ax.difference(Index(groupers), sort=False).tolist()
            self._reset_cache("_selected_obj")
