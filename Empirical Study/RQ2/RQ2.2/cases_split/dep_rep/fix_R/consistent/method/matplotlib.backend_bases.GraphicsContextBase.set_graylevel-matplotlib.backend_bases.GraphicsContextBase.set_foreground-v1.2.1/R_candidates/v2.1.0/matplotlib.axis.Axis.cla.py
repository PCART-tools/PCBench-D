    def cla(self):
        'clear the current axis'
        self.set_major_locator(mticker.AutoLocator())
        self.set_major_formatter(mticker.ScalarFormatter())
        self.set_minor_locator(mticker.NullLocator())
        self.set_minor_formatter(mticker.NullFormatter())

        self.set_label_text('')
        self._set_artist_props(self.label)

        # Keep track of setting to the default value, this allows use to know
        # if any of the following values is explicitly set by the user, so as
        # to not overwrite their settings with any of our 'auto' settings.
        self.isDefault_majloc = True
        self.isDefault_minloc = True
        self.isDefault_majfmt = True
        self.isDefault_minfmt = True
        self.isDefault_label = True

        # Clear the callback registry for this axis, or it may "leak"
        self.callbacks = cbook.CallbackRegistry()

        # whether the grids are on
        self._gridOnMajor = (rcParams['axes.grid'] and
                             rcParams['axes.grid.which'] in ('both', 'major'))
        self._gridOnMinor = (rcParams['axes.grid'] and
                             rcParams['axes.grid.which'] in ('both', 'minor'))

        self.label.set_text('')
        self._set_artist_props(self.label)

        self.reset_ticks()

        self.converter = None
        self.units = None
        self.set_units(None)
        self.stale = True
