    def locator_params(self, axis='both', tight=None, **kwargs):
        """
        Control behavior of tick locators.

        Parameters
        ----------
        axis : {'both', 'x', 'y'}, optional
            The axis on which to operate.

        tight : bool or None, optional
            Parameter passed to :meth:`autoscale_view`.
            Default is None, for no change.

        Other Parameters
        ----------------
        **kw :
            Remaining keyword arguments are passed to directly to the
            :meth:`~matplotlib.ticker.MaxNLocator.set_params` method.

        Typically one might want to reduce the maximum number
        of ticks and use tight bounds when plotting small
        subplots, for example::

            ax.locator_params(tight=True, nbins=4)

        Because the locator is involved in autoscaling,
        :meth:`autoscale_view` is called automatically after
        the parameters are changed.

        This presently works only for the
        :class:`~matplotlib.ticker.MaxNLocator` used
        by default on linear axes, but it may be generalized.
        """
        _x = axis in ['x', 'both']
        _y = axis in ['y', 'both']
        if _x:
            self.xaxis.get_major_locator().set_params(**kwargs)
        if _y:
            self.yaxis.get_major_locator().set_params(**kwargs)
        self.autoscale_view(tight=tight, scalex=_x, scaley=_y)
