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
        x, y : scalar or array-like
            The data positions.

        xerr, yerr : scalar or array-like, shape(N,) or shape(2,N), optional
            The errorbar sizes:

            - scalar: Symmetric +/- values for all data points.
            - shape(N,): Symmetric +/-values for each data point.
            - shape(2,N): Separate - and + values for each bar. First row
                contains the lower errors, the second row contains the
                upper errors.
            - *None*: No errorbar.

            See :doc:`/gallery/statistics/errorbar_features`
            for an example on the usage of ``xerr`` and ``yerr``.

        fmt : plot format string, optional, default: ''
            The format for the data points / data lines. See `.plot` for
            details.

            Use 'none' (case insensitive) to plot errorbars without any data
            markers.

        ecolor : mpl color, optional, default: None
            A matplotlib color arg which gives the color the errorbar lines.
            If None, use the color of the line connecting the markers.

        elinewidth : scalar, optional, default: None
            The linewidth of the errorbar lines. If None, the linewidth of
            the current style is used.

        capsize : scalar, optional, default: None
            The length of the error bar caps in points. If None, it will take
            the value from :rc:`errorbar.capsize`.

        capthick : scalar, optional, default: None
            An alias to the keyword argument *markeredgewidth* (a.k.a. *mew*).
            This setting is a more sensible name for the property that
            controls the thickness of the error bar cap in points. For
            backwards compatibility, if *mew* or *markeredgewidth* are given,
            then they will over-ride *capthick*. This may change in future
            releases.

        barsabove : bool, optional, default: False
            If True, will plot the errorbars above the plot
            symbols. Default is below.

        lolims, uplims, xlolims, xuplims : bool, optional, default: None
            These arguments can be used to indicate that a value gives only
            upper/lower limits. In that case a caret symbol is used to
            indicate this. *lims*-arguments may be of the same type as *xerr*
            and *yerr*.  To use limits with inverted axes, :meth:`set_xlim`
            or :meth:`set_ylim` must be called before :meth:`errorbar`.

        errorevery : positive integer, optional, default: 1
            Subsamples the errorbars. e.g., if errorevery=5, errorbars for
            every 5-th datapoint will be plotted. The data plot itself still
            shows all data points.

        Returns
        -------
        container : :class:`~.container.ErrorbarContainer`
            The container contains:

            - plotline: :class:`~matplotlib.lines.Line2D` instance of
              x, y plot markers and/or line.
            - caplines: A tuple of :class:`~matplotlib.lines.Line2D` instances
              of the error bar caps.
            - barlinecols: A tuple of
              :class:`~matplotlib.collections.LineCollection` with the
              horizontal and vertical error ranges.

        Other Parameters
        ----------------
        **kwargs :
            All other keyword arguments are passed on to the plot
            command for the markers. For example, this code makes big red
            squares with thick green edges::

                x,y,yerr = rand(3,10)
                errorbar(x, y, yerr, marker='s', mfc='red',
                         mec='green', ms=20, mew=4)

            where *mfc*, *mec*, *ms* and *mew* are aliases for the longer
            property names, *markerfacecolor*, *markeredgecolor*, *markersize*
            and *markeredgewidth*.

            Valid kwargs for the marker properties are `.Lines2D` properties:

            %(Line2D)s

        Notes
        -----
        .. [Notes section required for data comment. See #10189.]

        """
        kwargs = cbook.normalize_kwargs(kwargs, mlines.Line2D._alias_map)
        # anything that comes in as 'None', drop so the default thing
        # happens down stream
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        kwargs.setdefault('zorder', 2)

        if errorevery < 1:
            raise ValueError(
                'errorevery has to be a strictly positive integer')

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

        if ('color' in kwargs or 'color' in fmt_style_kwargs or
                ecolor is not None):
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
        if not iterable(x):
            x = [x]

        if not iterable(y):
            y = [y]

        if xerr is not None:
            if not iterable(xerr):
                xerr = [xerr] * len(x)

        if yerr is not None:
            if not iterable(yerr):
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

        everymask = np.arange(len(x)) % errorevery == 0

        def xywhere(xs, ys, mask):
            """
            return xs[mask], ys[mask] where mask is True but xs and
            ys are not arrays
            """
            assert len(xs) == len(ys)
            assert len(xs) == len(mask)
            xs = [thisx for thisx, b in zip(xs, mask) if b]
            ys = [thisy for thisy, b in zip(ys, mask) if b]
            return xs, ys

        def extract_err(err, data):
            '''private function to compute error bars

            Parameters
            ----------
            err : iterable
                xerr or yerr from errorbar
            data : iterable
                x or y from errorbar
            '''
            try:
                a, b = err
            except (TypeError, ValueError):
                pass
            else:
                if iterable(a) and iterable(b):
                    # using list comps rather than arrays to preserve units
                    low = [thisx - thiserr for thisx, thiserr
                           in cbook.safezip(data, a)]
                    high = [thisx + thiserr for thisx, thiserr
                            in cbook.safezip(data, b)]
                    return low, high
            # Check if xerr is scalar or symmetric. Asymmetric is handled
            # above. This prevents Nx2 arrays from accidentally
            # being accepted, when the user meant the 2xN transpose.
            # special case for empty lists
            if len(err) > 1:
                fe = safe_first_element(err)
                if len(err) != len(data) or np.size(fe) > 1:
                    raise ValueError("err must be [ scalar | N, Nx1 "
                                     "or 2xN array-like ]")
            # using list comps rather than arrays to preserve units
            low = [thisx - thiserr for thisx, thiserr
                   in cbook.safezip(data, err)]
            high = [thisx + thiserr for thisx, thiserr
                    in cbook.safezip(data, err)]
            return low, high

        if xerr is not None:
            left, right = extract_err(xerr, x)
            # select points without upper/lower limits in x and
            # draw normal errorbars for these points
            noxlims = ~(xlolims | xuplims)
            if noxlims.any() or len(noxlims) == 0:
                yo, _ = xywhere(y, right, noxlims & everymask)
                lo, ro = xywhere(left, right, noxlims & everymask)
                barcols.append(self.hlines(yo, lo, ro, **eb_lines_style))
                if capsize > 0:
                    caplines.append(mlines.Line2D(lo, yo, marker='|',
                                                  **eb_cap_style))
                    caplines.append(mlines.Line2D(ro, yo, marker='|',
                                                  **eb_cap_style))

            if xlolims.any():
                yo, _ = xywhere(y, right, xlolims & everymask)
                lo, ro = xywhere(x, right, xlolims & everymask)
                barcols.append(self.hlines(yo, lo, ro, **eb_lines_style))
                rightup, yup = xywhere(right, y, xlolims & everymask)
                if self.xaxis_inverted():
                    marker = mlines.CARETLEFTBASE
                else:
                    marker = mlines.CARETRIGHTBASE
                caplines.append(
                    mlines.Line2D(rightup, yup, ls='None', marker=marker,
                                  **eb_cap_style))
                if capsize > 0:
                    xlo, ylo = xywhere(x, y, xlolims & everymask)
                    caplines.append(mlines.Line2D(xlo, ylo, marker='|',
                                                  **eb_cap_style))

            if xuplims.any():
                yo, _ = xywhere(y, right, xuplims & everymask)
                lo, ro = xywhere(left, x, xuplims & everymask)
                barcols.append(self.hlines(yo, lo, ro, **eb_lines_style))
                leftlo, ylo = xywhere(left, y, xuplims & everymask)
                if self.xaxis_inverted():
                    marker = mlines.CARETRIGHTBASE
                else:
                    marker = mlines.CARETLEFTBASE
                caplines.append(
                    mlines.Line2D(leftlo, ylo, ls='None', marker=marker,
                                  **eb_cap_style))
                if capsize > 0:
                    xup, yup = xywhere(x, y, xuplims & everymask)
                    caplines.append(mlines.Line2D(xup, yup, marker='|',
                                                  **eb_cap_style))

        if yerr is not None:
            lower, upper = extract_err(yerr, y)
            # select points without upper/lower limits in y and
            # draw normal errorbars for these points
            noylims = ~(lolims | uplims)
            if noylims.any() or len(noylims) == 0:
                xo, _ = xywhere(x, lower, noylims & everymask)
                lo, uo = xywhere(lower, upper, noylims & everymask)
                barcols.append(self.vlines(xo, lo, uo, **eb_lines_style))
                if capsize > 0:
                    caplines.append(mlines.Line2D(xo, lo, marker='_',
                                                  **eb_cap_style))
                    caplines.append(mlines.Line2D(xo, uo, marker='_',
                                                  **eb_cap_style))

            if lolims.any():
                xo, _ = xywhere(x, lower, lolims & everymask)
                lo, uo = xywhere(y, upper, lolims & everymask)
                barcols.append(self.vlines(xo, lo, uo, **eb_lines_style))
                xup, upperup = xywhere(x, upper, lolims & everymask)
                if self.yaxis_inverted():
                    marker = mlines.CARETDOWNBASE
                else:
                    marker = mlines.CARETUPBASE
                caplines.append(
                    mlines.Line2D(xup, upperup, ls='None', marker=marker,
                                  **eb_cap_style))
                if capsize > 0:
                    xlo, ylo = xywhere(x, y, lolims & everymask)
                    caplines.append(mlines.Line2D(xlo, ylo, marker='_',
                                                  **eb_cap_style))

            if uplims.any():
                xo, _ = xywhere(x, lower, uplims & everymask)
                lo, uo = xywhere(lower, y, uplims & everymask)
                barcols.append(self.vlines(xo, lo, uo, **eb_lines_style))
                xlo, lowerlo = xywhere(x, lower, uplims & everymask)
                if self.yaxis_inverted():
                    marker = mlines.CARETUPBASE
                else:
                    marker = mlines.CARETDOWNBASE
                caplines.append(
                    mlines.Line2D(xlo, lowerlo, ls='None', marker=marker,
                                  **eb_cap_style))
                if capsize > 0:
                    xup, yup = xywhere(x, y, uplims & everymask)
                    caplines.append(mlines.Line2D(xup, yup, marker='_',
                                                  **eb_cap_style))
        for l in caplines:
            self.add_line(l)

        self.autoscale_view()
        errorbar_container = ErrorbarContainer((data_line, tuple(caplines),
                                                tuple(barcols)),
                                               has_xerr=(xerr is not None),
                                               has_yerr=(yerr is not None),
                                               label=label)
        self.containers.append(errorbar_container)

        return errorbar_container  # (l0, caplines, barcols)
