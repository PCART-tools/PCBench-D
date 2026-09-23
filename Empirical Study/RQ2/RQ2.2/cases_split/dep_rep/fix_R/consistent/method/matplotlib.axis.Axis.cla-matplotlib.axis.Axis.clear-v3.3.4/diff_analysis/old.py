    def cla(self):
        """Clear this axis."""

        self.label.set_text('')  # self.set_label_text would change isDefault_

        self._set_scale('linear')

        # Clear the callback registry for this axis, or it may "leak"
        self.callbacks = cbook.CallbackRegistry()

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
