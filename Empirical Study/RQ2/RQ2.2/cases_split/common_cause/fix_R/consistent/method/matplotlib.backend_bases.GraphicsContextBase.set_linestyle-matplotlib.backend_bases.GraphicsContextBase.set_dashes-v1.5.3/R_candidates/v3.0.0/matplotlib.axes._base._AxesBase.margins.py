    def margins(self, *margins, x=None, y=None, tight=True):
        """
        Set or retrieve autoscaling margins.

        The padding added to each limit of the axes is the *margin*
        times the data interval. All input parameters must be floats
        within the range [0, 1]. Passing both positional and keyword
        arguments is invalid and will raise a TypeError. If no
        arguments (positional or otherwise) are provided, the current
        margins will remain in place and simply be returned.

        Specifying any margin changes only the autoscaling; for example,
        if *xmargin* is not None, then *xmargin* times the X data
        interval will be added to each end of that interval before
        it is used in autoscaling.

        Parameters
        ----------
        args : float, optional
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

        tight : bool, default is True
            The *tight* parameter is passed to :meth:`autoscale_view`,
            which is executed after a margin is changed; the default
            here is *True*, on the assumption that when margins are
            specified, no additional padding to match tick marks is
            usually desired.  Set *tight* to *None* will preserve
            the previous setting.


        Returns
        -------
        xmargin, ymargin : float

        Notes
        -----
        If a previously used Axes method such as :meth:`pcolor` has set
        :attr:`use_sticky_edges` to `True`, only the limits not set by
        the "sticky artists" will be modified. To force all of the
        margins to be set, set :attr:`use_sticky_edges` to `False`
        before calling :meth:`margins`.

        """

        if margins and x is not None and y is not None:
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
                warnings.warn('ignoring tight=%r in get mode' % (tight,),
                              stacklevel=2)
            return self._xmargin, self._ymargin

        if x is not None:
            self.set_xmargin(x)
        if y is not None:
            self.set_ymargin(y)

        self.autoscale_view(
            tight=tight, scalex=(x is not None), scaley=(y is not None)
        )
