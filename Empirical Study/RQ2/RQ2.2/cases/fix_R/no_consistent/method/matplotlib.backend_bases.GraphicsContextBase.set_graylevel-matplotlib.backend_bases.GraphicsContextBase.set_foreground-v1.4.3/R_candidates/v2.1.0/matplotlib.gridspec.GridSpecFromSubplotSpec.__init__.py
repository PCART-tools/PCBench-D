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

        GridSpecBase.__init__(self, nrows, ncols,
                              width_ratios=width_ratios,
                              height_ratios=height_ratios)
