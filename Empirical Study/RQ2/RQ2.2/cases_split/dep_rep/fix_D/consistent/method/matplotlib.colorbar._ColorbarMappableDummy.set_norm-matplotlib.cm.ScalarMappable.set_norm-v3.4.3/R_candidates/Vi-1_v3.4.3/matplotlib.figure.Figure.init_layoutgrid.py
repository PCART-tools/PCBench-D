    def init_layoutgrid(self):
        """Initialize the layoutgrid for use in constrained_layout."""
        del(self._layoutgrid)
        self._layoutgrid = layoutgrid.LayoutGrid(
            parent=None, name='figlb')
