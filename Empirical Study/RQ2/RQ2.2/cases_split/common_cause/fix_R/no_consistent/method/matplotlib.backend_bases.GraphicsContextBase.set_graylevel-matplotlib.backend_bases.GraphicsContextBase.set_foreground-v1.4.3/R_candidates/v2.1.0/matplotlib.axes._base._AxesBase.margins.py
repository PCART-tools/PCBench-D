    def margins(self, *args, **kw):
        """
        Set or retrieve autoscaling margins.

        signatures::

            margins()

        returns xmargin, ymargin

        ::

            margins(margin)

            margins(xmargin, ymargin)

            margins(x=xmargin, y=ymargin)

            margins(..., tight=False)

        All three forms above set the xmargin and ymargin parameters.
        All keyword parameters are optional.  A single argument
        specifies both xmargin and ymargin.  The *tight* parameter
        is passed to :meth:`autoscale_view`, which is executed after
        a margin is changed; the default here is *True*, on the
        assumption that when margins are specified, no additional
        padding to match tick marks is usually desired.  Setting
        *tight* to *None* will preserve the previous setting.

        Specifying any margin changes only the autoscaling; for example,
        if *xmargin* is not None, then *xmargin* times the X data
        interval will be added to each end of that interval before
        it is used in autoscaling.

        """
        if not args and not kw:
            return self._xmargin, self._ymargin

        tight = kw.pop('tight', True)
        mx = kw.pop('x', None)
        my = kw.pop('y', None)
        if len(args) == 1:
            mx = my = args[0]
        elif len(args) == 2:
            mx, my = args
        elif len(args) > 2:
            raise ValueError("more than two arguments were supplied")
        if mx is not None:
            self.set_xmargin(mx)
        if my is not None:
            self.set_ymargin(my)

        scalex = (mx is not None)
        scaley = (my is not None)

        self.autoscale_view(tight=tight, scalex=scalex, scaley=scaley)
