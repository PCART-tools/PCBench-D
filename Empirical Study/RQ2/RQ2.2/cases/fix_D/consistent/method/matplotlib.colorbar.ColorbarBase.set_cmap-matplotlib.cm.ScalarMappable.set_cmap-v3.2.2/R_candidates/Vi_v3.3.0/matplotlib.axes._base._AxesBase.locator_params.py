    def locator_params(self, axis='both', tight=None, **kwargs):
        """
        Control behavior of major tick locators.

        Because the locator is involved in autoscaling, `~.Axes.autoscale_view`
        is called automatically after the parameters are changed.

        Parameters
        ----------
        axis : {'both', 'x', 'y'}, default: 'both'
            The axis on which to operate.

        tight : bool or None, optional
            Parameter passed to `~.Axes.autoscale_view`.
            Default is None, for no change.

        Other Parameters
        ----------------
        **kwargs
            Remaining keyword arguments are passed to directly to the
            ``set_params()`` method of the locator. Supported keywords depend
            on the type of the locator. See for example
            `~.ticker.MaxNLocator.set_params` for the `.ticker.MaxNLocator`
            used by default for linear axes.

        Examples
        --------
        When plotting small subplots, one might want to reduce the maximum
        number of ticks and use tight bounds, for example::

            ax.locator_params(tight=True, nbins=4)

        """
        cbook._check_in_list(['x', 'y', 'both'], axis=axis)
        update_x = axis in ['x', 'both']
        update_y = axis in ['y', 'both']
        if update_x:
            self.xaxis.get_major_locator().set_params(**kwargs)
        if update_y:
            self.yaxis.get_major_locator().set_params(**kwargs)
        self._request_autoscale_view(tight=tight,
                                     scalex=update_x, scaley=update_y)
        self.stale = True
