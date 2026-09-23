    @docstring.dedent_interpd
    def semilogy(self, *args, **kwargs):
        r"""Make a plot with log scaling on the `y` axis.

        Parameters
        ----------
        basey : scalar > 1
            Base of the `y` logarithm.

        subsy : None or iterable
            The location of the minor yticks. None defaults to
            autosubs, which depend on the number of decades in the
            plot. See :meth:`~matplotlib.axes.Axes.set_yscale` for
            details.

        nonposy : {'mask' | 'clip'} str
            Non-positive values in `y` can be masked as
            invalid, or clipped to a very small positive number.

        Returns
        -------
        `~matplotlib.lines.Line2D`
            Line instance of the plot.

        Other Parameters
        ----------------
        **kwargs :
            This function supports all the keyword arguments of
            :func:`~matplotlib.pyplot.plot` and
            :meth:`matplotlib.axes.Axes.set_xscale`.

            Keyword arguments also control the
            :class:`~matplotlib.lines.Line2D` properties:

            %(Line2D)s
        """
        if not self._hold:
            self.cla()
        d = {'basey': kwargs.pop('basey', 10),
             'subsy': kwargs.pop('subsy', None),
             }
        self.set_yscale('log', **d)
        b = self._hold
        self._hold = True  # we've already processed the hold
        l = self.plot(*args, **kwargs)
        self._hold = b  # restore the hold

        return l
