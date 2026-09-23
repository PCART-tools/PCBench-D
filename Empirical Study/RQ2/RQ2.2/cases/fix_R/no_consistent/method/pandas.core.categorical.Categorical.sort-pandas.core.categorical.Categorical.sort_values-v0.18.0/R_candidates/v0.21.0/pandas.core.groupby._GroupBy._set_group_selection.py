    def _set_group_selection(self):
        """
        Create group based selection. Used when selection is not passed
        directly but instead via a grouper.
        """
        grp = self.grouper
        if self.as_index and getattr(grp, 'groupings', None) is not None and \
           self.obj.ndim > 1:
            ax = self.obj._info_axis
            groupers = [g.name for g in grp.groupings
                        if g.level is None and g.in_axis]

            if len(groupers):
                self._group_selection = ax.difference(Index(groupers)).tolist()
                # GH12839 clear selected obj cache when group selection changes
                self._reset_cache('_selected_obj')
