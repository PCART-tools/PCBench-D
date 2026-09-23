    @_preprocess_data()
    @_docstring.dedent_interpd
    def bar(self, x, height, width=0.8, bottom=None, *, align="center",
            **kwargs):
        r"""
        Make a bar plot.

        The bars are positioned at *x* with the given *align*\ment. Their
        dimensions are given by *height* and *width*. The vertical baseline
        is *bottom* (default 0).

        Many parameters can take either a single value applying to all bars
        or a sequence of values, one for each bar.

        Parameters
        ----------
        x : float or array-like
            The x coordinates of the bars. See also *align* for the
            alignment of the bars to the coordinates.

        height : float or array-like
            The height(s) of the bars.

            Note that if *bottom* has units (e.g. datetime), *height* should be in
            units that are a difference from the value of *bottom* (e.g. timedelta).

        width : float or array-like, default: 0.8
            The width(s) of the bars.

            Note that if *x* has units (e.g. datetime), then *width* should be in
            units that are a difference (e.g. timedelta) around the *x* values.

        bottom : float or array-like, default: 0
            The y coordinate(s) of the bottom side(s) of the bars.

            Note that if *bottom* has units, then the y-axis will get a Locator and
            Formatter appropriate for the units (e.g. dates, or categorical).

        align : {'center', 'edge'}, default: 'center'
            Alignment of the bars to the *x* coordinates:

            - 'center': Center the base on the *x* positions.
            - 'edge': Align the left edges of the bars with the *x* positions.

            To align the bars on the right edge pass a negative *width* and
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

        label : str or list of str, optional
            A single label is attached to the resulting `.BarContainer` as a
            label for the whole dataset.
            If a list is provided, it must be the same length as *x* and
            labels the individual bars. Repeated labels are not de-duplicated
            and will cause repeated label entries, so this is best used when
            bars also differ in style (e.g., by passing a list to *color*.)

        xerr, yerr : float or array-like of shape(N,) or shape(2, N), optional
            If not *None*, add horizontal / vertical errorbars to the bar tips.
            The values are +/- sizes relative to the data:

            - scalar: symmetric +/- values for all bars
            - shape(N,): symmetric +/- values for each bar
            - shape(2, N): Separate - and + values for each bar. First row
              contains the lower errors, the second row contains the upper
              errors.
            - *None*: No errorbar. (Default)

            See :doc:`/gallery/statistics/errorbar_features` for an example on
            the usage of *xerr* and *yerr*.

        ecolor : color or list of color, default: 'black'
            The line color of the errorbars.

        capsize : float, default: :rc:`errorbar.capsize`
           The length of the error bar caps in points.

        error_kw : dict, optional
            Dictionary of keyword arguments to be passed to the
            `~.Axes.errorbar` method. Values of *ecolor* or *capsize* defined
            here take precedence over the independent keyword arguments.

        log : bool, default: False
            If *True*, set the y-axis to be log scale.

        data : indexable object, optional
            DATA_PARAMETER_PLACEHOLDER

        **kwargs : `.Rectangle` properties

        %(Rectangle:kwdoc)s

        See Also
        --------
        barh : Plot a horizontal bar plot.

        Notes
        -----
        Stacked bars can be achieved by passing individual *bottom* values per
        bar. See :doc:`/gallery/lines_bars_and_markers/bar_stacked`.
        """
        kwargs = cbook.normalize_kwargs(kwargs, mpatches.Patch)
        color = kwargs.pop('color', None)
        if color is None:
            color = self._get_patches_for_fill.get_next_color()
        edgecolor = kwargs.pop('edgecolor', None)
        linewidth = kwargs.pop('linewidth', None)
        hatch = kwargs.pop('hatch', None)

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
        capsize = kwargs.pop('capsize', mpl.rcParams["errorbar.capsize"])
        error_kw.setdefault('ecolor', ecolor)
        error_kw.setdefault('capsize', capsize)

        # The keyword argument *orientation* is used by barh() to defer all
        # logic and drawing to bar(). It is considered internal and is
        # intentionally not mentioned in the docstring.
        orientation = kwargs.pop('orientation', 'vertical')
        _api.check_in_list(['vertical', 'horizontal'], orientation=orientation)
        log = kwargs.pop('log', False)
        label = kwargs.pop('label', '')
        tick_labels = kwargs.pop('tick_label', None)

        y = bottom  # Matches barh call signature.
        if orientation == 'vertical':
            if y is None:
                y = 0
        else:  # horizontal
            if x is None:
                x = 0

        if orientation == 'vertical':
            # It is possible for y (bottom) to contain unit information.
            # However, it is also possible for y=0 for the default and height
            # to contain unit information.  This will prioritize the units of y.
            self._process_unit_info(
                [("x", x), ("y", y), ("y", height)], kwargs, convert=False)
            if log:
                self.set_yscale('log', nonpositive='clip')
        else:  # horizontal
            # It is possible for x (left) to contain unit information.
            # However, it is also possible for x=0 for the default and width
            # to contain unit information.  This will prioritize the units of x.
            self._process_unit_info(
                [("x", x), ("x", width), ("y", y)], kwargs, convert=False)
            if log:
                self.set_xscale('log', nonpositive='clip')

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

        x, height, width, y, linewidth, hatch = np.broadcast_arrays(
            # Make args iterable too.
            np.atleast_1d(x), height, width, y, linewidth, hatch)

        # Now that units have been converted, set the tick locations.
        if orientation == 'vertical':
            tick_label_axis = self.xaxis
            tick_label_position = x
        else:  # horizontal
            tick_label_axis = self.yaxis
            tick_label_position = y

        if not isinstance(label, str) and np.iterable(label):
            bar_container_label = '_nolegend_'
            patch_labels = label
        else:
            bar_container_label = label
            patch_labels = ['_nolegend_'] * len(x)
        if len(patch_labels) != len(x):
            raise ValueError(f'number of labels ({len(patch_labels)}) '
                             f'does not match number of bars ({len(x)}).')

        linewidth = itertools.cycle(np.atleast_1d(linewidth))
        hatch = itertools.cycle(np.atleast_1d(hatch))
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
        _api.check_in_list(['center', 'edge'], align=align)
        if align == 'center':
            if orientation == 'vertical':
                try:
                    left = x - width / 2
                except TypeError as e:
                    raise TypeError(f'the dtypes of parameters x ({x.dtype}) '
                                    f'and width ({width.dtype}) '
                                    f'are incompatible') from e
                bottom = y
            else:  # horizontal
                try:
                    bottom = y - height / 2
                except TypeError as e:
                    raise TypeError(f'the dtypes of parameters y ({y.dtype}) '
                                    f'and height ({height.dtype}) '
                                    f'are incompatible') from e
                left = x
        else:  # edge
            left = x
            bottom = y

        patches = []
        args = zip(left, bottom, width, height, color, edgecolor, linewidth,
                   hatch, patch_labels)
        for l, b, w, h, c, e, lw, htch, lbl in args:
            r = mpatches.Rectangle(
                xy=(l, b), width=w, height=h,
                facecolor=c,
                edgecolor=e,
                linewidth=lw,
                label=lbl,
                hatch=htch,
                )
            r._internal_update(kwargs)
            r.get_path()._interpolation_steps = 100
            if orientation == 'vertical':
                r.sticky_edges.y.append(b)
            else:  # horizontal
                r.sticky_edges.x.append(l)
            self.add_patch(r)
            patches.append(r)

        if xerr is not None or yerr is not None:
            if orientation == 'vertical':
                # using list comps rather than arrays to preserve unit info
                ex = [l + 0.5 * w for l, w in zip(left, width)]
                ey = [b + h for b, h in zip(bottom, height)]

            else:  # horizontal
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

        if orientation == 'vertical':
            datavalues = height
        else:  # horizontal
            datavalues = width

        bar_container = BarContainer(patches, errorbar, datavalues=datavalues,
                                     orientation=orientation,
                                     label=bar_container_label)
        self.add_container(bar_container)

        if tick_labels is not None:
            tick_labels = np.broadcast_to(tick_labels, len(patches))
            tick_label_axis.set_ticks(tick_label_position)
            tick_label_axis.set_ticklabels(tick_labels)

        return bar_container
