    @docstring.dedent_interpd
    def semilogx(self, *args, **kwargs):
        """
        Make a plot with log scaling on the *x* axis.

        Parameters
        ----------
        basex : float, optional
            Base of the *x* logarithm. The scalar should be larger
            than 1.

        subsx : array_like, optional
            The location of the minor xticks; *None* defaults to
            autosubs, which depend on the number of decades in the
            plot; see :meth:`~matplotlib.axes.Axes.set_xscale` for
            details.

        nonposx : string, optional, {'mask', 'clip'}
            Non-positive values in *x* can be masked as
            invalid, or clipped to a very small positive number.

        Returns
        -------
        `~matplotlib.pyplot.plot`
            Log-scaled plot on the *x* axis.

        Other Parameters
        ----------------
        **kwargs :
            Keyword arguments control the :class:`~matplotlib.lines.Line2D`
            properties:

            %(Line2D)s

        Notes
        -----
        This function supports all the keyword arguments of
        :func:`~matplotlib.pyplot.plot` and
        :meth:`matplotlib.axes.Axes.set_xscale`.
        """
        if not self._hold:
            self.cla()
        d = {'basex': kwargs.pop('basex', 10),
             'subsx': kwargs.pop('subsx', None),
             }

        self.set_xscale('log', **d)
        b = self._hold
        self._hold = True  # we've already processed the hold
        l = self.plot(*args, **kwargs)
        self._hold = b  # restore the hold
        return l
