    @_preprocess_data()
    @docstring.dedent_interpd
    def bar(self, x, height, width=0.8, bottom=None, *, align="center",
            **kwargs):
        r"""
        Make a bar plot.

        The bars are positioned at *x* with the given *align*\ment. Their
        dimensions are given by *width* and *height*. The vertical baseline
        is *bottom* (default 0).

        Each of *x*, *height*, *width*, and *bottom* may either be a scalar
        applying to all bars, or it may be a sequence of length N providing a
        separate value for each bar.

        Parameters
        ----------
        x : sequence of scalars
            The x coordinates of the bars. See also *align* for the
            alignment of the bars to the coordinates.

        height : scalar or sequence of scalars
            The height(s) of the bars.

        width : scalar or array-like, optional
            The width(s) of the bars (default: 0.8).

        bottom : scalar or array-like, optional
            The y coordinate(s) of the bars bases (default: 0).

        align : {'center', 'edge'}, optional, default: 'center'
            Alignment of the bars to the *x* coordinates:

            - 'center': Center the base on the *x* positions.
            - 'edge': Align the left edges of the bars with the *x* positions.

            To align the bars on the right edge pass a negative *width* and
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
            If not *None*, add horizontal / vertical errorbars to the bar tips.
            The values are +/- sizes relative to the data:

            - scalar: symmetric +/- values for all bars
            - shape(N,): symmetric +/- values for each bar
            - shape(2, N): Separate - and + values for each bar. First row
              contains the lower errors, the second row contains the upper
              errors.
            - *None*: No errorbar. (Default)

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
            If *True*, set the y-axis to be log scale.

        orientation : {'vertical',  'horizontal'}, optional
            *This is for internal use only.* Please use `barh` for
            horizontal bar plots. Default: 'vertical'.

        See also
        --------
        barh: Plot a horizontal bar plot.

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
        kwargs = cbook.normalize_kwargs(kwargs, mpatches.Patch)
        color = kwargs.pop('color', None)
        if color is None:
            color = self._get_patches_for_fill.get_next_color()
        edgecolor = kwargs.pop('edgecolor', None)
        linewidth = kwargs.pop('linewidth', None)

        # Because xerr and yerr will be passed to errorbar, most dimension
        # checking and processing will be left to the errorbar method.
        xerr = kwargs.pop('xerr', None)
        yerr = kwargs.pop('yerr', None)
        error_kw = kwargs.pop('error_kw', {})
        ezorder = error_kw.pop('zorder', None)
        if ezorder is None:
            ezorder = kwargs.get('zorder', None)
            if ezorder is not None:
                # If using the bar zorder, increment slightly to make sure
                # errorbars are drawn on top of bars
                ezorder += 0.01
        error_kw.setdefault('zorder', ezorder)
        ecolor = kwargs.pop('ecolor', 'k')
        capsize = kwargs.pop('capsize', rcParams["errorbar.capsize"])
        error_kw.setdefault('ecolor', ecolor)
        error_kw.setdefault('capsize', capsize)

        orientation = kwargs.pop('orientation', 'vertical')
        cbook._check_in_list(['vertical', 'horizontal'],
                             orientation=orientation)
        log = kwargs.pop('log', False)
        label = kwargs.pop('label', '')
        tick_labels = kwargs.pop('tick_label', None)

        y = bottom  # Matches barh call signature.
        if orientation == 'vertical':
            if y is None:
                y = 0
        elif orientation == 'horizontal':
            if x is None:
                x = 0

        if orientation == 'vertical':
            self._process_unit_info(xdata=x, ydata=height, kwargs=kwargs)
            if log:
                self.set_yscale('log', nonposy='clip')
        elif orientation == 'horizontal':
            self._process_unit_info(xdata=width, ydata=y, kwargs=kwargs)
            if log:
                self.set_xscale('log', nonposx='clip')

        # lets do some conversions now since some types cannot be
        # subtracted uniformly
        if self.xaxis is not None:
            x0 = x
            x = np.asarray(self.convert_xunits(x))
            width = self._convert_dx(width, x0, x, self.convert_xunits)
            if xerr is not None:
                xerr = self._convert_dx(xerr, x0, x, self.convert_xunits)
        if self.yaxis is not None:
            y0 = y
            y = np.asarray(self.convert_yunits(y))
            height = self._convert_dx(height, y0, y, self.convert_yunits)
            if yerr is not None:
                yerr = self._convert_dx(yerr, y0, y, self.convert_yunits)

        x, height, width, y, linewidth = np.broadcast_arrays(
            # Make args iterable too.
            np.atleast_1d(x), height, width, y, linewidth)

        # Now that units have been converted, set the tick locations.
        if orientation == 'vertical':
            tick_label_axis = self.xaxis
            tick_label_position = x
        elif orientation == 'horizontal':
            tick_label_axis = self.yaxis
            tick_label_position = y

        linewidth = itertools.cycle(np.atleast_1d(linewidth))
        color = itertools.chain(itertools.cycle(mcolors.to_rgba_array(color)),
                                # Fallback if color == "none".
                                itertools.repeat('none'))
        if edgecolor is None:
            edgecolor = itertools.repeat(None)
        else:
            edgecolor = itertools.chain(
                itertools.cycle(mcolors.to_rgba_array(edgecolor)),
                # Fallback if edgecolor == "none".
                itertools.repeat('none'))

        # We will now resolve the alignment and really have
        # left, bottom, width, height vectors
        cbook._check_in_list(['center', 'edge'], align=align)
        if align == 'center':
            if orientation == 'vertical':
                try:
                    left = x - width / 2
                except TypeError as e:
                    raise TypeError(f'the dtypes of parameters x ({x.dtype}) '
                                    f'and width ({width.dtype}) '
                                    f'are incompatible') from e
                bottom = y
            elif orientation == 'horizontal':
                try:
                    bottom = y - height / 2
                except TypeError as e:
                    raise TypeError(f'the dtypes of parameters y ({y.dtype}) '
                                    f'and height ({height.dtype}) '
                                    f'are incompatible') from e
                left = x
        elif align == 'edge':
            left = x
            bottom = y

        patches = []
        args = zip(left, bottom, width, height, color, edgecolor, linewidth)
        for l, b, w, h, c, e, lw in args:
            r = mpatches.Rectangle(
                xy=(l, b), width=w, height=h,
                facecolor=c,
                edgecolor=e,
                linewidth=lw,
                label='_nolegend_',
                )
            r.update(kwargs)
            r.get_path()._interpolation_steps = 100
            if orientation == 'vertical':
                r.sticky_edges.y.append(b)
            elif orientation == 'horizontal':
                r.sticky_edges.x.append(l)
            self.add_patch(r)
            patches.append(r)

        if xerr is not None or yerr is not None:
            if orientation == 'vertical':
                # using list comps rather than arrays to preserve unit info
                ex = [l + 0.5 * w for l, w in zip(left, width)]
                ey = [b + h for b, h in zip(bottom, height)]

            elif orientation == 'horizontal':
                # using list comps rather than arrays to preserve unit info
                ex = [l + w for l, w in zip(left, width)]
                ey = [b + 0.5 * h for b, h in zip(bottom, height)]

            error_kw.setdefault("label", '_nolegend_')

            errorbar = self.errorbar(ex, ey,
                                     yerr=yerr, xerr=xerr,
                                     fmt='none', **error_kw)
        else:
            errorbar = None

        self._request_autoscale_view()

        bar_container = BarContainer(patches, errorbar, label=label)
        self.add_container(bar_container)

        if tick_labels is not None:
            tick_labels = np.broadcast_to(tick_labels, len(patches))
            tick_label_axis.set_ticks(tick_label_position)
            tick_label_axis.set_ticklabels(tick_labels)

        return bar_container
