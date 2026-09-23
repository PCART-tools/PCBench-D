    @docstring.dedent_interpd
    def loglog(self, *args, **kwargs):
        """
        Make a plot with log scaling on both the x and y axis.

        Call signatures::

            loglog([x], y, [fmt], data=None, **kwargs)
            loglog([x], y, [fmt], [x2], y2, [fmt2], ..., **kwargs)

        This is just a thin wrapper around `.plot` which additionally changes
        both the x-axis and the y-axis to log scaling. All of the concepts and
        parameters of plot can be used here as well.

        The additional parameters *basex/y*, *subsx/y* and *nonposx/y* control
        the x/y-axis properties. They are just forwarded to `.Axes.set_xscale`
        and `.Axes.set_yscale`.

        Parameters
        ----------
        basex, basey : scalar, optional, default 10
            Base of the x/y logarithm.

        subsx, subsy : sequence, optional
            The location of the minor x/y ticks. If *None*, reasonable
            locations are automatically chosen depending on the number of
            decades in the plot.
            See `.Axes.set_xscale` / `.Axes.set_yscale` for details.

        nonposx, nonposy : {'mask', 'clip'}, optional, default 'mask'
            Non-positive values in x or y can be masked as invalid, or clipped
            to a very small positive number.

        Returns
        -------
        lines
            A list of `.Line2D` objects representing the plotted data.

        Other Parameters
        ----------------
        **kwargs
            All parameters supported by `.plot`.
        """
        dx = {k: kwargs.pop(k) for k in ['basex', 'subsx', 'nonposx']
              if k in kwargs}
        dy = {k: kwargs.pop(k) for k in ['basey', 'subsy', 'nonposy']
              if k in kwargs}

        self.set_xscale('log', **dx)
        self.set_yscale('log', **dy)

        l = self.plot(*args, **kwargs)
        return l
