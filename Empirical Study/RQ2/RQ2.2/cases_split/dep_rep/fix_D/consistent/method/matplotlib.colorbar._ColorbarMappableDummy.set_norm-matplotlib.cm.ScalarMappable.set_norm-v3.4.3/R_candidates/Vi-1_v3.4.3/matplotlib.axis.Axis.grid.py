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
        TOGGLE = object()
        UNSET = object()
        visible = kwargs.pop('visible', UNSET)

        if b is None:
            if visible is UNSET:
                if kwargs:  # grid(color='r')
                    b = True
                else:  # grid()
                    b = TOGGLE
            else:  # grid(visible=v)
                b = visible
        else:
            if visible is not UNSET and bool(b) != bool(visible):
                # grid(True, visible=False), grid(False, visible=True)
                raise ValueError(
                    "'b' and 'visible' specify inconsistent grid visibilities")
            if kwargs and not b:  # something false-like but not None
                # grid(0, visible=True)
                _api.warn_external('First parameter to grid() is false, '
                                   'but line properties are supplied. The '
                                   'grid will be enabled.')
                b = True

        which = which.lower()
        _api.check_in_list(['major', 'minor', 'both'], which=which)
        gridkw = {'grid_' + item[0]: item[1] for item in kwargs.items()}
        if which in ['minor', 'both']:
            gridkw['gridOn'] = (not self._minor_tick_kw['gridOn']
                                if b is TOGGLE else b)
            self.set_tick_params(which='minor', **gridkw)
        if which in ['major', 'both']:
            gridkw['gridOn'] = (not self._major_tick_kw['gridOn']
                                if b is TOGGLE else b)
            self.set_tick_params(which='major', **gridkw)
        self.stale = True
