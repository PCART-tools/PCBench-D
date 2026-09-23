    def __init__(self, nrows, ncols,
                 subplot_spec,
                 wspace=None, hspace=None,
                 height_ratios=None, width_ratios=None):
        """
        The number of rows and number of columns of the grid need to
        be set. An instance of SubplotSpec is also needed to be set
        from which the layout parameters will be inherited. The wspace
        and hspace of the layout can be optionally specified or the
        default values (from the figure or rcParams) will be used.
        """
        self._wspace = wspace
        self._hspace = hspace
        self._subplot_spec = subplot_spec
        self.figure = self._subplot_spec.get_gridspec().figure
        super().__init__(nrows, ncols,
                         width_ratios=width_ratios,
                         height_ratios=height_ratios)
        # do the layoutgrids for constrained_layout:
        subspeclb = subplot_spec.get_gridspec()._layoutgrid
        if subspeclb is None:
            self._layoutgrid = None
        else:
            # this _toplayoutbox is a container that spans the cols and
            # rows in the parent gridspec.  Not yet implemented,
            # but we do this so that it is possible to have subgridspec
            # level artists.
            self._toplayoutgrid = layoutgrid.LayoutGrid(
                parent=subspeclb,
                name=subspeclb.name + '.top' + layoutgrid.seq_id(),
                nrows=1, ncols=1,
                parent_pos=(subplot_spec.rowspan, subplot_spec.colspan))
            self._layoutgrid = layoutgrid.LayoutGrid(
                    parent=self._toplayoutgrid,
                    name=(self._toplayoutgrid.name + '.gridspec' +
                          layoutgrid.seq_id()),
                    nrows=nrows, ncols=ncols,
                    width_ratios=width_ratios, height_ratios=height_ratios)
