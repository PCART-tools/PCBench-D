    @_preprocess_data(replace_names=["x", "y", "xerr", "yerr"],
                      label_namer="y")
    @docstring.dedent_interpd
    def errorbar(self, x, y, yerr=None, xerr=None,
                 fmt='', ecolor=None, elinewidth=None, capsize=None,
                 barsabove=False, lolims=False, uplims=False,
                 xlolims=False, xuplims=False, errorevery=1, capthick=None,
                 **kwargs):
        """
        Plot y versus x as lines and/or markers with attached errorbars.

        *x*, *y* define the data locations, *xerr*, *yerr* define the errorbar
        sizes. By default, this draws the data markers/lines as well the
        errorbars. Use fmt='none' to draw errorbars without any data markers.

        Parameters
        ----------
        x, y : float or array-like
            The data positions.

        xerr, yerr : float or array-like, shape(N,) or shape(2, N), optional
            The errorbar sizes:

            - scalar: Symmetric +/- values for all data points.
            - shape(N,): Symmetric +/-values for each data point.
            - shape(2, N): Separate - and + values for each bar. First row
              contains the lower errors, the second row contains the upper
              errors.
            - *None*: No errorbar.

            Note that all error arrays should have *positive* values.

            See :doc:`/gallery/statistics/errorbar_features`
            for an example on the usage of ``xerr`` and ``yerr``.

        fmt : str, default: ''
            The format for the data points / data lines. See `.plot` for
            details.

            Use 'none' (case insensitive) to plot errorbars without any data
            markers.

        ecolor : color, default: None
            The color of the errorbar lines.  If None, use the color of the
            line connecting the markers.

        elinewidth : float, default: None
            The linewidth of the errorbar lines. If None, the linewidth of
            the current style is used.

        capsize : float, default: :rc:`errorbar.capsize`
            The length of the error bar caps in points.

        capthick : float, default: None
            An alias to the keyword argument *markeredgewidth* (a.k.a. *mew*).
            This setting is a more sensible name for the property that
            controls the thickness of the error bar cap in points. For
            backwards compatibility, if *mew* or *markeredgewidth* are given,
            then they will over-ride *capthick*. This may change in future
            releases.

        barsabove : bool, default: False
            If True, will plot the errorbars above the plot
            symbols. Default is below.

        lolims, uplims, xlolims, xuplims : bool, default: False
            These arguments can be used to indicate that a value gives only
            upper/lower limits.  In that case a caret symbol is used to
            indicate this. *lims*-arguments may be scalars, or array-likes of
            the same length as *xerr* and *yerr*.  To use limits with inverted
            axes, `~.Axes.set_xlim` or `~.Axes.set_ylim` must be called before
            :meth:`errorbar`.  Note the tricky parameter names: setting e.g.
            *lolims* to True means that the y-value is a *lower* limit of the
            True value, so, only an *upward*-pointing arrow will be drawn!

        errorevery : int or (int, int), default: 1
            draws error bars on a subset of the data. *errorevery* =N draws
            error bars on the points (x[::N], y[::N]).
            *errorevery* =(start, N) draws error bars on the points
            (x[start::N], y[start::N]). e.g. errorevery=(6, 3)
            adds error bars to the data at (x[6], x[9], x[12], x[15], ...).
            Used to avoid overlapping error bars when two series share x-axis
            values.

        Returns
        -------
        `.ErrorbarContainer`
            The container contains:

            - plotline: `.Line2D` instance of x, y plot markers and/or line.
            - caplines: A tuple of `.Line2D` instances of the error bar caps.
            - barlinecols: A tuple of `.LineCollection` with the horizontal and
              vertical error ranges.

        Other Parameters
        ----------------
        **kwargs
            All other keyword arguments are passed on to the `~.Axes.plot` call
            drawing the markers. For example, this code makes big red squares
            with thick green edges::

                x, y, yerr = rand(3, 10)
                errorbar(x, y, yerr, marker='s', mfc='red',
                         mec='green', ms=20, mew=4)

            where *mfc*, *mec*, *ms* and *mew* are aliases for the longer
            property names, *markerfacecolor*, *markeredgecolor*, *markersize*
            and *markeredgewidth*.

            Valid kwargs for the marker properties are `.Line2D` properties:

            %(_Line2D_docstr)s
        """
        kwargs = cbook.normalize_kwargs(kwargs, mlines.Line2D)
        # anything that comes in as 'None', drop so the default thing
        # happens down stream
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        kwargs.setdefault('zorder', 2)

        try:
            offset, errorevery = errorevery
        except TypeError:
            offset = 0

        if errorevery < 1 or int(errorevery) != errorevery:
            raise ValueError(
                'errorevery must be positive integer or tuple of integers')
        if int(offset) != offset:
            raise ValueError("errorevery's starting index must be an integer")

        self._process_unit_info(xdata=x, ydata=y, kwargs=kwargs)

        plot_line = (fmt.lower() != 'none')
        label = kwargs.pop("label", None)

        if fmt == '':
            fmt_style_kwargs = {}
        else:
            fmt_style_kwargs = {k: v for k, v in
                                zip(('linestyle', 'marker', 'color'),
                                    _process_plot_format(fmt))
                                if v is not None}
        if fmt == 'none':
            # Remove alpha=0 color that _process_plot_format returns
            fmt_style_kwargs.pop('color')

        if ('color' in kwargs or 'color' in fmt_style_kwargs):
            base_style = {}
            if 'color' in kwargs:
                base_style['color'] = kwargs.pop('color')
        else:
            base_style = next(self._get_lines.prop_cycler)

        base_style['label'] = '_nolegend_'
        base_style.update(fmt_style_kwargs)
        if 'color' not in base_style:
            base_style['color'] = 'C0'
        if ecolor is None:
            ecolor = base_style['color']
        # make sure all the args are iterable; use lists not arrays to
        # preserve units
        if not np.iterable(x):
            x = [x]

        if not np.iterable(y):
            y = [y]

        if len(x) != len(y):
            raise ValueError("'x' and 'y' must have the same size")

        if xerr is not None:
            if not np.iterable(xerr):
                xerr = [xerr] * len(x)

        if yerr is not None:
            if not np.iterable(yerr):
                yerr = [yerr] * len(y)

        # make the style dict for the 'normal' plot line
        plot_line_style = {
            **base_style,
            **kwargs,
            'zorder': (kwargs['zorder'] - .1 if barsabove else
                       kwargs['zorder'] + .1),
        }

        # make the style dict for the line collections (the bars)
        eb_lines_style = dict(base_style)
        eb_lines_style.pop('marker', None)
        eb_lines_style.pop('linestyle', None)
        eb_lines_style['color'] = ecolor

        if elinewidth:
            eb_lines_style['linewidth'] = elinewidth
        elif 'linewidth' in kwargs:
            eb_lines_style['linewidth'] = kwargs['linewidth']

        for key in ('transform', 'alpha', 'zorder', 'rasterized'):
            if key in kwargs:
                eb_lines_style[key] = kwargs[key]

        # set up cap style dictionary
        eb_cap_style = dict(base_style)
        # eject any marker information from format string
        eb_cap_style.pop('marker', None)
        eb_lines_style.pop('markerfacecolor', None)
        eb_lines_style.pop('markeredgewidth', None)
        eb_lines_style.pop('markeredgecolor', None)
        eb_cap_style.pop('ls', None)
        eb_cap_style['linestyle'] = 'none'
        if capsize is None:
            capsize = rcParams["errorbar.capsize"]
        if capsize > 0:
            eb_cap_style['markersize'] = 2. * capsize
        if capthick is not None:
            eb_cap_style['markeredgewidth'] = capthick

        # For backwards-compat, allow explicit setting of
        # 'markeredgewidth' to over-ride capthick.
        for key in ('markeredgewidth', 'transform', 'alpha',
                    'zorder', 'rasterized'):
            if key in kwargs:
                eb_cap_style[key] = kwargs[key]
        eb_cap_style['color'] = ecolor

        data_line = None
        if plot_line:
            data_line = mlines.Line2D(x, y, **plot_line_style)
            self.add_line(data_line)

        barcols = []
        caplines = []

        # arrays fine here, they are booleans and hence not units
        lolims = np.broadcast_to(lolims, len(x)).astype(bool)
        uplims = np.broadcast_to(uplims, len(x)).astype(bool)
        xlolims = np.broadcast_to(xlolims, len(x)).astype(bool)
        xuplims = np.broadcast_to(xuplims, len(x)).astype(bool)

        everymask = np.zeros(len(x), bool)
        everymask[offset::errorevery] = True

        def apply_mask(arrays, mask):
            # Return, for each array in *arrays*, the elements for which *mask*
            # is True, without using fancy indexing.
            return [[*itertools.compress(array, mask)] for array in arrays]

        def extract_err(name, err, data, lolims, uplims):
            """
            Private function to compute error bars.

            Parameters
            ----------
            name : {'x', 'y'}
                Name used in the error message.
            err : array-like
                xerr or yerr from errorbar().
            data : array-like
                x or y from errorbar().
            lolims : array-like
                Error is only applied on **upper** side when this is True.  See
                the note in the main docstring about this parameter's name.
            uplims : array-like
                Error is only applied on **lower** side when this is True.  See
                the note in the main docstring about this parameter's name.
            """
            try:  # Asymmetric error: pair of 1D iterables.
                a, b = err
                iter(a)
                iter(b)
            except (TypeError, ValueError):
                a = b = err  # Symmetric error: 1D iterable.
            if np.ndim(a) > 1 or np.ndim(b) > 1:
                raise ValueError(
                    f"{name}err must be a scalar or a 1D or (2, n) array-like")
            # Using list comprehensions rather than arrays to preserve units.
            for e in [a, b]:
                if len(data) != len(e):
                    raise ValueError(
                        f"The lengths of the data ({len(data)}) and the "
                        f"error {len(e)} do not match")
            low = [v if lo else v - e for v, e, lo in zip(data, a, lolims)]
            high = [v if up else v + e for v, e, up in zip(data, b, uplims)]
            return low, high

        if xerr is not None:
            left, right = extract_err('x', xerr, x, xlolims, xuplims)
            barcols.append(self.hlines(
                *apply_mask([y, left, right], everymask), **eb_lines_style))
            # select points without upper/lower limits in x and
            # draw normal errorbars for these points
            noxlims = ~(xlolims | xuplims)
            if noxlims.any() and capsize > 0:
                yo, lo, ro = apply_mask([y, left, right], noxlims & everymask)
                caplines.extend([
                    mlines.Line2D(lo, yo, marker='|', **eb_cap_style),
                    mlines.Line2D(ro, yo, marker='|', **eb_cap_style)])
            if xlolims.any():
                xo, yo, lo, ro = apply_mask([x, y, left, right],
                                            xlolims & everymask)
                if self.xaxis_inverted():
                    marker = mlines.CARETLEFTBASE
                else:
                    marker = mlines.CARETRIGHTBASE
                caplines.append(mlines.Line2D(
                    ro, yo, ls='None', marker=marker, **eb_cap_style))
                if capsize > 0:
                    caplines.append(mlines.Line2D(
                        xo, yo, marker='|', **eb_cap_style))
            if xuplims.any():
                xo, yo, lo, ro = apply_mask([x, y, left, right],
                                            xuplims & everymask)
                if self.xaxis_inverted():
                    marker = mlines.CARETRIGHTBASE
                else:
                    marker = mlines.CARETLEFTBASE
                caplines.append(mlines.Line2D(
                    lo, yo, ls='None', marker=marker, **eb_cap_style))
                if capsize > 0:
                    caplines.append(mlines.Line2D(
                        xo, yo, marker='|', **eb_cap_style))

        if yerr is not None:
            lower, upper = extract_err('y', yerr, y, lolims, uplims)
            barcols.append(self.vlines(
                *apply_mask([x, lower, upper], everymask), **eb_lines_style))
            # select points without upper/lower limits in y and
            # draw normal errorbars for these points
            noylims = ~(lolims | uplims)
            if noylims.any() and capsize > 0:
                xo, lo, uo = apply_mask([x, lower, upper], noylims & everymask)
                caplines.extend([
                    mlines.Line2D(xo, lo, marker='_', **eb_cap_style),
                    mlines.Line2D(xo, uo, marker='_', **eb_cap_style)])
            if lolims.any():
                xo, yo, lo, uo = apply_mask([x, y, lower, upper],
                                            lolims & everymask)
                if self.yaxis_inverted():
                    marker = mlines.CARETDOWNBASE
                else:
                    marker = mlines.CARETUPBASE
                caplines.append(mlines.Line2D(
                    xo, uo, ls='None', marker=marker, **eb_cap_style))
                if capsize > 0:
                    caplines.append(mlines.Line2D(
                        xo, yo, marker='_', **eb_cap_style))
            if uplims.any():
                xo, yo, lo, uo = apply_mask([x, y, lower, upper],
                                            uplims & everymask)
                if self.yaxis_inverted():
                    marker = mlines.CARETUPBASE
                else:
                    marker = mlines.CARETDOWNBASE
                caplines.append(mlines.Line2D(
                    xo, lo, ls='None', marker=marker, **eb_cap_style))
                if capsize > 0:
                    caplines.append(mlines.Line2D(
                        xo, yo, marker='_', **eb_cap_style))

        for l in caplines:
            self.add_line(l)

        self._request_autoscale_view()
        errorbar_container = ErrorbarContainer(
            (data_line, tuple(caplines), tuple(barcols)),
            has_xerr=(xerr is not None), has_yerr=(yerr is not None),
            label=label)
        self.containers.append(errorbar_container)

        return errorbar_container  # (l0, caplines, barcols)
