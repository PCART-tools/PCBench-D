    def init_layoutgrid(self):
        """Initialize the layoutgrid for use in constrained_layout."""
        if self._layoutgrid is None:
            gs = self._subplotspec.get_gridspec()
            parent = gs._layoutgrid
            if parent is not None:
                self._layoutgrid = layoutgrid.LayoutGrid(
                    parent=parent,
                    name=(parent.name + '.' + 'panellb' +
                          layoutgrid.seq_id()),
                    parent_inner=True,
                    nrows=1, ncols=1,
                    parent_pos=(self._subplotspec.rowspan,
                                self._subplotspec.colspan))
