    @docstring.dedent_interpd
    def barh(self, y, width, height=0.8, left=None, *, align="center",
             **kwargs):
        r"""
        Make a horizontal bar plot.

        The bars are positioned at *y* with the given *align*\ment. Their
        dimensions are given by *width* and *height*. The horizontal baseline
        is *left* (default 0).

        Each of *y*, *width*, *height*, and *left* may either be a scalar
        applying to all bars, or it may be a sequence of length N providing a
        separate value for each bar.

        Parameters
        ----------
        y : scalar or array-like
            The y coordinates of the bars. See also *align* for the
            alignment of the bars to the coordinates.

        width : scalar or array-like
            The width(s) of the bars.

        height : sequence of scalars, optional, default: 0.8
            The heights of the bars.

        left : sequence of scalars
            The x coordinates of the left sides of the bars (default: 0).

        align : {'center', 'edge'}, optional, default: 'center'
            Alignment of the base to the *y* coordinates*:

            - 'center': Center the bars on the *y* positions.
            - 'edge': Align the bottom edges of the bars with the *y*
              positions.

            To align the bars on the top edge pass a negative *height* and
            ``align='edge'``.

        Returns
        -------
        container : `.BarContainer`
            Container with all the bars and optionally errorbars.

        Other Parameters
        ----------------
        color : scalar or array-like, optional
            The colors of the bar faces.

        edgecolor : scalar or array-like, optional
            The colors of the bar edges.

        linewidth : scalar or array-like, optional
            Width of the bar edge(s). If 0, don't draw edges.

        tick_label : str or array-like, optional
            The tick labels of the bars.
            Default: None (Use default numeric labels.)

        xerr, yerr : scalar or array-like of shape(N,) or shape(2, N), optional
            If not ``None``, add horizontal / vertical errorbars to the
            bar tips. The values are +/- sizes relative to the data:

            - scalar: symmetric +/- values for all bars
            - shape(N,): symmetric +/- values for each bar
            - shape(2, N): Separate - and + values for each bar. First row
              contains the lower errors, the second row contains the upper
              errors.
            - *None*: No errorbar. (default)

            See :doc:`/gallery/statistics/errorbar_features`
            for an example on the usage of ``xerr`` and ``yerr``.

        ecolor : scalar or array-like, optional, default: 'black'
            The line color of the errorbars.

        capsize : scalar, optional
           The length of the error bar caps in points.
           Default: None, which will take the value from
           :rc:`errorbar.capsize`.

        error_kw : dict, optional
            Dictionary of kwargs to be passed to the `~.Axes.errorbar`
            method. Values of *ecolor* or *capsize* defined here take
            precedence over the independent kwargs.

        log : bool, optional, default: False
            If ``True``, set the x-axis to be log scale.

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
        kwargs.setdefault('orientation', 'horizontal')
        patches = self.bar(x=left, height=height, width=width, bottom=y,
                           align=align, **kwargs)
        return patches
