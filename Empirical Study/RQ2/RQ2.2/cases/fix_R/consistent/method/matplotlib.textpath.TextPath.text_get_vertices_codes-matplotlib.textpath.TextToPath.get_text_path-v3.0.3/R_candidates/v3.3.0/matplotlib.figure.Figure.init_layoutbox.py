    def init_layoutbox(self):
        """Initialize the layoutbox for use in constrained_layout."""
        if self._layoutbox is None:
            self._layoutbox = layoutbox.LayoutBox(
                parent=None, name='figlb', artist=self)
            self._layoutbox.constrain_geometry(0., 0., 1., 1.)
