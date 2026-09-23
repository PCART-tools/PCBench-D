    def grid(self, b=None, which='major', **kwargs):
        """
        Set the axis grid on or off; b is a boolean. Use *which* =
        'major' | 'minor' | 'both' to set the grid for major or minor ticks.

        If *b* is *None* and len(kwargs)==0, toggle the grid state.  If
        *kwargs* are supplied, it is assumed you want the grid on and *b*
        will be set to True.

        *kwargs* are used to set the line properties of the grids, e.g.,

          xax.grid(color='r', linestyle='-', linewidth=2)
        """
        if len(kwargs):
            b = True
        which = which.lower()
        if which in ['minor', 'both']:
            if b is None:
                self._gridOnMinor = not self._gridOnMinor
            else:
                self._gridOnMinor = b
            for tick in self.minorTicks:  # don't use get_ticks here!
                if tick is None:
                    continue
                tick.gridOn = self._gridOnMinor
                if len(kwargs):
                    tick.gridline.update(kwargs)
            self._minor_tick_kw['gridOn'] = self._gridOnMinor
        if which in ['major', 'both']:
            if b is None:
                self._gridOnMajor = not self._gridOnMajor
            else:
                self._gridOnMajor = b
            for tick in self.majorTicks:  # don't use get_ticks here!
                if tick is None:
                    continue
                tick.gridOn = self._gridOnMajor
                if len(kwargs):
                    tick.gridline.update(kwargs)
            self._major_tick_kw['gridOn'] = self._gridOnMajor
        self.stale = True
