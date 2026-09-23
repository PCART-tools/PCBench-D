    def clear(self):
        """
        Clear the axis.

        This resets axis properties to their default values:

        - the label
        - the scale
        - locators, formatters and ticks
        - major and minor grid
        - units
        - registered callbacks
        """
        self.label._reset_visual_defaults()
        self.offsetText._reset_visual_defaults()
        self.labelpad = mpl.rcParams['axes.labelpad']

        self._init()

        self._set_scale('linear')

        # Clear the callback registry for this axis, or it may "leak"
        self.callbacks = cbook.CallbackRegistry(signals=["units"])

        # whether the grids are on
        self._major_tick_kw['gridOn'] = (
                mpl.rcParams['axes.grid'] and
                mpl.rcParams['axes.grid.which'] in ('both', 'major'))
        self._minor_tick_kw['gridOn'] = (
                mpl.rcParams['axes.grid'] and
                mpl.rcParams['axes.grid.which'] in ('both', 'minor'))
        self.reset_ticks()

        self.converter = None
        self.units = None
        self.set_units(None)
        self.stale = True
