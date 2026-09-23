    def margins(self, *margins, x=None, y=None, tight=True):
        """
        Set or retrieve margins around the data for autoscaling axis limits.

        This allows to configure the padding around the data without having to
        set explicit limits using `~.Axes.set_xlim` / `~.Axes.set_ylim`.

        Autoscaling determines the axis limits by adding *margin* times the
        data interval as padding around the data. See the following illustration:

        .. plot:: _embedded_plots/axes_margins.py

        All input parameters must be floats greater than -0.5. Passing both
        positional and keyword arguments is invalid and will raise a TypeError.
        If no arguments (positional or otherwise) are provided, the current
        margins will remain unchanged and simply be returned.

        The default margins are :rc:`axes.xmargin` and :rc:`axes.ymargin`.

        Parameters
        ----------
        *margins : float, optional
            If a single positional argument is provided, it specifies
            both margins of the x-axis and y-axis limits. If two
            positional arguments are provided, they will be interpreted
            as *xmargin*, *ymargin*. If setting the margin on a single
            axis is desired, use the keyword arguments described below.

        x, y : float, optional
            Specific margin values for the x-axis and y-axis,
            respectively. These cannot be used with positional
            arguments, but can be used individually to alter on e.g.,
            only the y-axis.

        tight : bool or None, default: True
            The *tight* parameter is passed to `~.axes.Axes.autoscale_view`,
            which is executed after a margin is changed; the default
            here is *True*, on the assumption that when margins are
            specified, no additional padding to match tick marks is
            usually desired.  Setting *tight* to *None* preserves
            the previous setting.

        Returns
        -------
        xmargin, ymargin : float

        Notes
        -----
        If a previously used Axes method such as :meth:`pcolor` has set
        `~.Axes.use_sticky_edges` to `True`, only the limits not set by
        the "sticky artists" will be modified. To force all
        margins to be set, set `~.Axes.use_sticky_edges` to `False`
        before calling :meth:`margins`.

        See Also
        --------
        .Axes.set_xmargin, .Axes.set_ymargin
        """

        if margins and (x is not None or y is not None):
            raise TypeError('Cannot pass both positional and keyword '
                            'arguments for x and/or y.')
        elif len(margins) == 1:
            x = y = margins[0]
        elif len(margins) == 2:
            x, y = margins
        elif margins:
            raise TypeError('Must pass a single positional argument for all '
                            'margins, or one for each margin (x, y).')

        if x is None and y is None:
            if tight is not True:
                _api.warn_external(f'ignoring tight={tight!r} in get mode')
            return self._xmargin, self._ymargin

        if tight is not None:
            self._tight = tight
        if x is not None:
            self.set_xmargin(x)
        if y is not None:
            self.set_ymargin(y)
