    @_preprocess_data(replace_names=["x", "left",
                                     "height", "width",
                                     "y", "bottom",
                                     "color", "edgecolor", "linewidth",
                                     "tick_label", "xerr", "yerr",
                                     "ecolor"],
                      label_namer=None,
                      replace_all_args=True
                      )
    @docstring.dedent_interpd
    def bar(self, *args, **kwargs):
        """
        Make a bar plot.

        Call signatures::

           bar(x, height, *, align='center', **kwargs)
           bar(x, height, width, *, align='center', **kwargs)
           bar(x, height, width, bottom, *, align='center', **kwargs)

        Make a bar plot with rectangles bounded by

        .. math::

           (x - width/2, x + width/2, bottom, bottom + height)

        (left, right, bottom and top edges) by default.  *x*,
        *height*, *width*, and *bottom* can be either scalars or
        sequences.

        The *align* and *orientation* kwargs control the interpretation of *x*
        and *bottom*

        The *align* keyword-only argument controls if *x* is interpreted
        as the center or the left edge of the rectangle.

        Parameters
        ----------
        x : sequence of scalars
            the x coordinates of the bars.

            *align* controls if *x* is the bar center (default) or
            left edge.

        height : scalar or sequence of scalars
            the height(s) of the bars

        width : scalar or array-like, optional
            the width(s) of the bars
            default: 0.8

        bottom : scalar or array-like, optional
            the y coordinate(s) of the bars
            default: None

        align : {'center', 'edge'}, optional, default: 'center'
            If 'center', interpret the *x* argument as the coordinates
            of the centers of the bars.  If 'edge', aligns bars by
            their left edges

            To align the bars on the right edge pass a negative
            *width* and ``align='edge'``

        Returns
        -------
        bars : matplotlib.container.BarContainer
            Container with all of the bars + errorbars

        Other Parameters
        ----------------
        color : scalar or array-like, optional
            the colors of the bar faces

        edgecolor : scalar or array-like, optional
            the colors of the bar edges

        linewidth : scalar or array-like, optional
            width of bar edge(s). If None, use default
            linewidth; If 0, don't draw edges.
            default: None

        tick_label : string or array-like, optional
            the tick labels of the bars
            default: None

        xerr : scalar or array-like, optional
            if not None, will be used to generate errorbar(s) on the bar chart
            default: None

        yerr : scalar or array-like, optional
            if not None, will be used to generate errorbar(s) on the bar chart
            default: None

        ecolor : scalar or array-like, optional
            specifies the color of errorbar(s)
            default: None

        capsize : scalar, optional
           determines the length in points of the error bar caps
           default: None, which will take the value from the
           ``errorbar.capsize`` :data:`rcParam<matplotlib.rcParams>`.

        error_kw : dict, optional
            dictionary of kwargs to be passed to errorbar method. *ecolor* and
            *capsize* may be specified here rather than as independent kwargs.

        log : boolean, optional
            If true, sets the axis to be log scale.
            default: False

        orientation : {'vertical',  'horizontal'}, optional

            This is for internal use, please do not directly use this,
            call `barh` instead.

            The orientation of the bars.

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
        kwargs = cbook.normalize_kwargs(kwargs, mpatches._patch_alias_map)
        # this is using the lambdas to do the arg/kwarg unpacking rather
        # than trying to re-implement all of that logic our selves.
        matchers = [
            (lambda x, height, width=0.8, bottom=None, **kwargs:
             (False, x, height, width, bottom, kwargs)),
            (lambda left, height, width=0.8, bottom=None, **kwargs:
             (True, left, height, width, bottom, kwargs)),
        ]
        exps = []
        for matcher in matchers:
            try:
                dp, x, height, width, y, kwargs = matcher(*args, **kwargs)
            except TypeError as e:
                # This can only come from a no-match as there is
                # no other logic in the matchers.
                exps.append(e)
            else:
                break
        else:
            raise exps[0]
        # if we matched the second-case, then the user passed in
        # left=val as a kwarg which we want to deprecate
        if dp:
            warnings.warn(
                "The *left* kwarg to `bar` is deprecated use *x* instead. "
                "Support for *left* will be removed in Matplotlib 3.0",
                mplDeprecation, stacklevel=2)
        if not self._hold:
            self.cla()
        color = kwargs.pop('color', None)
        if color is None:
            color = self._get_patches_for_fill.get_next_color()
        edgecolor = kwargs.pop('edgecolor', None)
        linewidth = kwargs.pop('linewidth', None)

        # Because xerr and yerr will be passed to errorbar,
        # most dimension checking and processing will be left
        # to the errorbar method.
        xerr = kwargs.pop('xerr', None)
        yerr = kwargs.pop('yerr', None)
        error_kw = kwargs.pop('error_kw', dict())
        ecolor = kwargs.pop('ecolor', 'k')
        capsize = kwargs.pop('capsize', rcParams["errorbar.capsize"])
        error_kw.setdefault('ecolor', ecolor)
        error_kw.setdefault('capsize', capsize)

        if rcParams['_internal.classic_mode']:
            align = kwargs.pop('align', 'edge')
        else:
            align = kwargs.pop('align', 'center')

        orientation = kwargs.pop('orientation', 'vertical')
        log = kwargs.pop('log', False)
        label = kwargs.pop('label', '')
        tick_labels = kwargs.pop('tick_label', None)

        adjust_ylim = False
        adjust_xlim = False

        if orientation == 'vertical':
            if y is None:
                if self.get_yscale() == 'log':
                    adjust_ylim = True
                y = 0

        elif orientation == 'horizontal':
            if x is None:
                if self.get_xscale() == 'log':
                    adjust_xlim = True
                x = 0

        x, height, width, y, linewidth = np.broadcast_arrays(
            # Make args iterable too.
            np.atleast_1d(x), height, width, y, linewidth)

        if orientation == 'vertical':
            self._process_unit_info(xdata=x, ydata=height, kwargs=kwargs)
            if log:
                self.set_yscale('log', nonposy='clip')

            tick_label_axis = self.xaxis
            tick_label_position = x
        elif orientation == 'horizontal':
            self._process_unit_info(xdata=width, ydata=y, kwargs=kwargs)
            if log:
                self.set_xscale('log', nonposx='clip')

            tick_label_axis = self.yaxis
            tick_label_position = y
        else:
            raise ValueError('invalid orientation: %s' % orientation)

        linewidth = itertools.cycle(np.atleast_1d(linewidth))
        color = itertools.chain(itertools.cycle(mcolors.to_rgba_array(color)),
                                # Fallback if color == "none".
                                itertools.repeat([0, 0, 0, 0]))
        if edgecolor is None:
            edgecolor = itertools.repeat(None)
        else:
            edgecolor = itertools.chain(mcolors.to_rgba_array(edgecolor),
                                        # Fallback if edgecolor == "none".
                                        itertools.repeat([0, 0, 0, 0]))

        # lets do some conversions now since some types cannot be
        # subtracted uniformly
        if self.xaxis is not None:
            x = self.convert_xunits(x)
            width = self.convert_xunits(width)
            if xerr is not None:
                xerr = self.convert_xunits(xerr)

        if self.yaxis is not None:
            y = self.convert_yunits(y)
            height = self.convert_yunits(height)
            if yerr is not None:
                yerr = self.convert_yunits(yerr)

        # We will now resolve the alignment and really have
        # left, bottom, width, height vectors
        if align == 'center':
            if orientation == 'vertical':
                left = x - width / 2
                bottom = y
            elif orientation == 'horizontal':
                bottom = y - height / 2
                left = x
        elif align == 'edge':
            left = x
            bottom = y
        else:
            raise ValueError('invalid alignment: %s' % align)

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

        holdstate = self._hold
        self._hold = True  # ensure hold is on before plotting errorbars

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

        self._hold = holdstate  # restore previous hold state

        if adjust_xlim:
            xmin, xmax = self.dataLim.intervalx
            xmin = min(w for w in width if w > 0)
            if xerr is not None:
                xmin = xmin - np.max(xerr)
            xmin = max(xmin * 0.9, 1e-100)
            self.dataLim.intervalx = (xmin, xmax)

        if adjust_ylim:
            ymin, ymax = self.dataLim.intervaly
            ymin = min(h for h in height if h > 0)
            if yerr is not None:
                ymin = ymin - np.max(yerr)
            ymin = max(ymin * 0.9, 1e-100)
            self.dataLim.intervaly = (ymin, ymax)
        self.autoscale_view()

        bar_container = BarContainer(patches, errorbar, label=label)
        self.add_container(bar_container)

        if tick_labels is not None:
            tick_labels = _backports.broadcast_to(tick_labels, len(patches))
            tick_label_axis.set_ticks(tick_label_position)
            tick_label_axis.set_ticklabels(tick_labels)

        return bar_container
