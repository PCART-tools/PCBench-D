    @docstring.dedent_interpd
    def barh(self, *args, **kwargs):
        """
        Make a horizontal bar plot.

        Call signatures::

           bar(y, width, *, align='center', **kwargs)
           bar(y, width, height, *, align='center', **kwargs)
           bar(y, width, height, left, *, align='center', **kwargs)

        Make a horizontal bar plot with rectangles by default bounded by

        .. math::

           (left, left + width, y - height/2, y + height/2)

        (left, right, bottom and top edges) by default.  *y*, *width*,
        *height*, and *left* can be either scalars or sequences.

        The *align* keyword-only argument controls if *y* is interpreted
        as the center or the bottom edge of the rectangle.


        Parameters
        ----------
        y : scalar or array-like
            the y coordinate(s) of the bars

            *align* controls if *y* is the bar center (default)
            or bottom edge.

        width : scalar or array-like
            the width(s) of the bars

        height : sequence of scalars, optional, default: 0.8
            the heights of the bars

        left : sequence of scalars
            the x coordinates of the left sides of the bars

        align : {'center', 'edge'}, optional, default: 'center'
            If 'center', interpret the *y* argument as the coordinates
            of the centers of the bars.  If 'edge', aligns bars by
            their bottom edges

            To align the bars on the top edge pass a negative
            *height* and ``align='edge'``

        Returns
        -------
        `matplotlib.patches.Rectangle` instances.

        Other Parameters
        ----------------
        color : scalar or array-like, optional
            the colors of the bars

        edgecolor : scalar or array-like, optional
            the colors of the bar edges

        linewidth : scalar or array-like, optional, default: None
            width of bar edge(s). If None, use default
            linewidth; If 0, don't draw edges.

        tick_label : string or array-like, optional, default: None
            the tick labels of the bars

        xerr : scalar or array-like, optional, default: None
            if not None, will be used to generate errorbar(s) on the bar chart

        yerr : scalar or array-like, optional, default: None
            if not None, will be used to generate errorbar(s) on the bar chart

        ecolor : scalar or array-like, optional, default: None
            specifies the color of errorbar(s)

        capsize : scalar, optional
           determines the length in points of the error bar caps
           default: None, which will take the value from the
           ``errorbar.capsize`` :data:`rcParam<matplotlib.rcParams>`.

        error_kw :
            dictionary of kwargs to be passed to errorbar method. `ecolor` and
            `capsize` may be specified here rather than as independent kwargs.

        log : boolean, optional, default: False
            If true, sets the axis to be log scale

        See also
        --------
        bar: Plot a vertical bar plot.

        Notes
        -----
        The optional arguments *color*, *edgecolor*, *linewidth*,
        *xerr*, and *yerr* can be either scalars or sequences of
        length equal to the number of bars.  This enables you to use
        bar as the basis for stacked bar charts, or candlestick plots.
        Detail: *xerr* and *yerr* are passed directly to
        :meth:`errorbar`, so they can also have shape 2xN for
        independent specification of lower and upper errors.

        Other optional kwargs:

        %(Rectangle)s

        """
        # this is using the lambdas to do the arg/kwarg unpacking rather
        # than trying to re-implement all of that logic our selves.
        matchers = [
            (lambda y, width, height=0.8, left=None, **kwargs:
             (False, y, width, height, left, kwargs)),
            (lambda bottom, width, height=0.8, left=None, **kwargs:
             (True, bottom, width, height, left, kwargs)),
        ]
        excs = []
        for matcher in matchers:
            try:
                dp, y, width, height, left, kwargs = matcher(*args, **kwargs)
            except TypeError as e:
                # This can only come from a no-match as there is
                # no other logic in the matchers.
                excs.append(e)
            else:
                break
        else:
            raise excs[0]

        if dp:
            warnings.warn(
                "The *bottom* kwarg to `barh` is deprecated use *y* instead. "
                "Support for *bottom* will be removed in Matplotlib 3.0",
                mplDeprecation, stacklevel=2)
        kwargs.setdefault('orientation', 'horizontal')
        patches = self.bar(x=left, height=height, width=width,
                           bottom=y, **kwargs)
        return patches
