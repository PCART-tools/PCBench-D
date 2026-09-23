    @docstring.dedent_interpd
    def barh(self, y, width, height=0.8, left=None, *, align="center",
             **kwargs):
        r"""
        Make a horizontal bar plot.

        The bars are positioned at *y* with the given *align*\ment. Their
        dimensions are given by *width* and *height*. The horizontal baseline
        is *left* (default 0).

        Many parameters can take either a single value applying to all bars
        or a sequence of values, one for each bar.

        Parameters
        ----------
        y : float or array-like
            The y coordinates of the bars. See also *align* for the
            alignment of the bars to the coordinates.

        width : float or array-like
            The width(s) of the bars.

        height : float or array-like, default: 0.8
            The heights of the bars.

        left : float or array-like, default: 0
            The x coordinates of the left sides of the bars.

        align : {'center', 'edge'}, default: 'center'
            Alignment of the base to the *y* coordinates*:

            - 'center': Center the bars on the *y* positions.
            - 'edge': Align the bottom edges of the bars with the *y*
              positions.

            To align the bars on the top edge pass a negative *height* and
            ``align='edge'``.

        Returns
        -------
        `.BarContainer`
            Container with all the bars and optionally errorbars.

        Other Parameters
        ----------------
        color : color or list of color, optional
            The colors of the bar faces.

        edgecolor : color or list of color, optional
            The colors of the bar edges.

        linewidth : float or array-like, optional
            Width of the bar edge(s). If 0, don't draw edges.

        tick_label : str or list of str, optional
            The tick labels of the bars.
            Default: None (Use default numeric labels.)

        xerr, yerr : float or array-like of shape(N,) or shape(2, N), optional
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

        ecolor : color or list of color, default: 'black'
            The line color of the errorbars.

        capsize : float, default: :rc:`errorbar.capsize`
           The length of the error bar caps in points.

        error_kw : dict, optional
            Dictionary of kwargs to be passed to the `~.Axes.errorbar`
            method. Values of *ecolor* or *capsize* defined here take
            precedence over the independent kwargs.

        log : bool, default: False
            If ``True``, set the x-axis to be log scale.

        **kwargs : `.Rectangle` properties

        %(Rectangle)s

        See Also
        --------
        bar: Plot a vertical bar plot.

        Notes
        -----
        Stacked bars can be achieved by passing individual *left* values per
        bar. See
        :doc:`/gallery/lines_bars_and_markers/horizontal_barchart_distribution`
        .
        """
        kwargs.setdefault('orientation', 'horizontal')
        patches = self.bar(x=left, height=height, width=width, bottom=y,
                           align=align, **kwargs)
        return patches
