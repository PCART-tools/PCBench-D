    def _set_selection_from_grouper(self):
        """ we may need create a selection if we have non-level groupers """
        grp = self.grouper
        if self.as_index and getattr(grp,'groupings',None) is not None and self.obj.ndim > 1:
            ax = self.obj._info_axis
            groupers = [ g.name for g in grp.groupings if g.level is None and g.name is not None and g.name in ax ]
            if len(groupers):
                self._group_selection = ax.difference(Index(groupers)).tolist()
