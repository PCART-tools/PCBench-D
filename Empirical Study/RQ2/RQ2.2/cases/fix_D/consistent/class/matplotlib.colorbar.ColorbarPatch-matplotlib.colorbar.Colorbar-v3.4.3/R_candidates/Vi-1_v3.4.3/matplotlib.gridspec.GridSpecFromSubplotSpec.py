class GridSpecFromSubplotSpec(GridSpecBase):
    """
    GridSpec whose subplot layout parameters are inherited from the
    location specified by a given SubplotSpec.
    """
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

    def get_subplot_params(self, figure=None):
        """Return a dictionary of subplot layout parameters."""
        hspace = (self._hspace if self._hspace is not None
                  else figure.subplotpars.hspace if figure is not None
                  else rcParams["figure.subplot.hspace"])
        wspace = (self._wspace if self._wspace is not None
                  else figure.subplotpars.wspace if figure is not None
                  else rcParams["figure.subplot.wspace"])

        figbox = self._subplot_spec.get_position(figure)
        left, bottom, right, top = figbox.extents

        return mpl.figure.SubplotParams(left=left, right=right,
                                        bottom=bottom, top=top,
                                        wspace=wspace, hspace=hspace)

    def get_topmost_subplotspec(self):
        """
        Return the topmost `.SubplotSpec` instance associated with the subplot.
        """
        return self._subplot_spec.get_topmost_subplotspec()
