    def grid(self, b=None, which='major', **kwargs):
        """
        Configure the grid lines.

        Parameters
        ----------
        b : bool or None
            Whether to show the grid lines. If any *kwargs* are supplied,
            it is assumed you want the grid on and *b* will be set to True.

            If *b* is *None* and there are no *kwargs*, this toggles the
            visibility of the lines.

        which : {'major', 'minor', 'both'}
            The grid lines to apply the changes on.

        **kwargs : `.Line2D` properties
            Define the line properties of the grid, e.g.::

                grid(color='r', linestyle='-', linewidth=2)

        """
        if len(kwargs):
            b = True
        which = which.lower()
        gridkw = {'grid_' + item[0]: item[1] for item in kwargs.items()}
        if which in ['minor', 'both']:
            if b is None:
                self._gridOnMinor = not self._gridOnMinor
            else:
                self._gridOnMinor = b
            self.set_tick_params(which='minor', gridOn=self._gridOnMinor,
                                 **gridkw)
        if which in ['major', 'both']:
            if b is None:
                self._gridOnMajor = not self._gridOnMajor
            else:
                self._gridOnMajor = b
            self.set_tick_params(which='major', gridOn=self._gridOnMajor,
                                 **gridkw)
        self.stale = True
