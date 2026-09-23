    @docstring.dedent_interpd
    def semilogy(self, *args, **kwargs):
        """
        Make a plot with log scaling on the y axis.

        Call signatures::

            semilogy([x], y, [fmt], data=None, **kwargs)
            semilogy([x], y, [fmt], [x2], y2, [fmt2], ..., **kwargs)

        This is just a thin wrapper around `.plot` which additionally changes
        the y-axis to log scaling. All of the concepts and parameters of plot
        can be used here as well.

        The additional parameters *basey*, *subsy* and *nonposy* control the
        y-axis properties. They are just forwarded to `.Axes.set_yscale`.

        Parameters
        ----------
        basey : scalar, optional, default 10
            Base of the y logarithm.

        subsy : array_like, optional
            The location of the minor yticks. If *None*, reasonable locations
            are automatically chosen depending on the number of decades in the
            plot. See `.Axes.set_yscale` for details.

        nonposy : {'mask', 'clip'}, optional, default 'mask'
            Non-positive values in y can be masked as invalid, or clipped to a
            very small positive number.

        Returns
        -------
        lines
            A list of `~.Line2D` objects representing the plotted data.

        Other Parameters
        ----------------
        **kwargs
            All parameters supported by `.plot`.
        """
        d = {k: kwargs.pop(k) for k in ['basey', 'subsy', 'nonposy']
             if k in kwargs}
        self.set_yscale('log', **d)
        l = self.plot(*args, **kwargs)

        return l
