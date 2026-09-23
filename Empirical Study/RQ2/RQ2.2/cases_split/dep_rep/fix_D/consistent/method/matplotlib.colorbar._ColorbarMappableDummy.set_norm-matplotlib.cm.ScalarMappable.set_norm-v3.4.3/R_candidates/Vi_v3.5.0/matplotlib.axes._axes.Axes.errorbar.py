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
        data : indexable object, optional
            DATA_PARAMETER_PLACEHOLDER

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

            %(Line2D:kwdoc)s
        """
        kwargs = cbook.normalize_kwargs(kwargs, mlines.Line2D)
        # Drop anything that comes in as None to use the default instead.
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        kwargs.setdefault('zorder', 2)

        # Casting to object arrays preserves units.
        if not isinstance(x, np.ndarray):
            x = np.asarray(x, dtype=object)
        if not isinstance(y, np.ndarray):
            y = np.asarray(y, dtype=object)
        if xerr is not None and not isinstance(xerr, np.ndarray):
            xerr = np.asarray(xerr, dtype=object)
        if yerr is not None and not isinstance(yerr, np.ndarray):
            yerr = np.asarray(yerr, dtype=object)
        x, y = np.atleast_1d(x, y)  # Make sure all the args are iterable.
        if len(x) != len(y):
            raise ValueError("'x' and 'y' must have the same size")

        if isinstance(errorevery, Integral):
            errorevery = (0, errorevery)
        if isinstance(errorevery, tuple):
            if (len(errorevery) == 2 and
                    isinstance(errorevery[0], Integral) and
                    isinstance(errorevery[1], Integral)):
                errorevery = slice(errorevery[0], None, errorevery[1])
            else:
                raise ValueError(
                    f'errorevery={errorevery!r} is a not a tuple of two '
                    f'integers')
        elif isinstance(errorevery, slice):
            pass
        elif not isinstance(errorevery, str) and np.iterable(errorevery):
            # fancy indexing
            try:
                x[errorevery]
            except (ValueError, IndexError) as err:
                raise ValueError(
                    f"errorevery={errorevery!r} is iterable but not a valid "
                    f"NumPy fancy index to match 'xerr'/'yerr'") from err
        else:
            raise ValueError(
                f"errorevery={errorevery!r} is not a recognized value")
        everymask = np.zeros(len(x), bool)
        everymask[errorevery] = True

        label = kwargs.pop("label", None)
        kwargs['label'] = '_nolegend_'

        # Create the main line and determine overall kwargs for child artists.
        # We avoid calling self.plot() directly, or self._get_lines(), because
        # that would call self._process_unit_info again, and do other indirect
        # data processing.
        (data_line, base_style), = self._get_lines._plot_args(
            (x, y) if fmt == '' else (x, y, fmt), kwargs, return_kwargs=True)

        # Do this after creating `data_line` to avoid modifying `base_style`.
        if barsabove:
            data_line.set_zorder(kwargs['zorder'] - .1)
        else:
            data_line.set_zorder(kwargs['zorder'] + .1)

        # Add line to plot, or throw it away and use it to determine kwargs.
        if fmt.lower() != 'none':
            self.add_line(data_line)
        else:
            data_line = None
            # Remove alpha=0 color that _get_lines._plot_args returns for
            # 'none' format, and replace it with user-specified color, if
            # supplied.
            base_style.pop('color')
            if 'color' in kwargs:
                base_style['color'] = kwargs.pop('color')

        if 'color' not in base_style:
            base_style['color'] = 'C0'
        if ecolor is None:
            ecolor = base_style['color']

        # Eject any line-specific information from format string, as it's not
        # needed for bars or caps.
        for key in ['marker', 'markersize', 'markerfacecolor',
                    'markeredgewidth', 'markeredgecolor', 'markevery',
                    'linestyle', 'fillstyle', 'drawstyle', 'dash_capstyle',
                    'dash_joinstyle', 'solid_capstyle', 'solid_joinstyle']:
            base_style.pop(key, None)

        # Make the style dict for the line collections (the bars).
        eb_lines_style = {**base_style, 'color': ecolor}

        if elinewidth is not None:
            eb_lines_style['linewidth'] = elinewidth
        elif 'linewidth' in kwargs:
            eb_lines_style['linewidth'] = kwargs['linewidth']

        for key in ('transform', 'alpha', 'zorder', 'rasterized'):
            if key in kwargs:
                eb_lines_style[key] = kwargs[key]

        # Make the style dict for caps (the "hats").
        eb_cap_style = {**base_style, 'linestyle': 'none'}
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

        barcols = []
        caplines = []

        # Vectorized fancy-indexer.
        def apply_mask(arrays, mask): return [array[mask] for array in arrays]

        # dep: dependent dataset, indep: independent dataset
        for (dep_axis, dep, err, lolims, uplims, indep, lines_func,
             marker, lomarker, himarker) in [
                ("x", x, xerr, xlolims, xuplims, y, self.hlines,
                 "|", mlines.CARETRIGHTBASE, mlines.CARETLEFTBASE),
                ("y", y, yerr, lolims, uplims, x, self.vlines,
                 "_", mlines.CARETUPBASE, mlines.CARETDOWNBASE),
        ]:
            if err is None:
                continue
            lolims = np.broadcast_to(lolims, len(dep)).astype(bool)
            uplims = np.broadcast_to(uplims, len(dep)).astype(bool)
            try:
                np.broadcast_to(err, (2, len(dep)))
            except ValueError:
                raise ValueError(
                    f"'{dep_axis}err' (shape: {np.shape(err)}) must be a "
                    f"scalar or a 1D or (2, n) array-like whose shape matches "
                    f"'{dep_axis}' (shape: {np.shape(dep)})") from None
            # This is like
            #     elow, ehigh = np.broadcast_to(...)
            #     return dep - elow * ~lolims, dep + ehigh * ~uplims
            # except that broadcast_to would strip units.
            low, high = dep + np.row_stack([-(1 - lolims), 1 - uplims]) * err

            barcols.append(lines_func(
                *apply_mask([indep, low, high], everymask), **eb_lines_style))
            # Normal errorbars for points without upper/lower limits.
            nolims = ~(lolims | uplims)
            if nolims.any() and capsize > 0:
                indep_masked, lo_masked, hi_masked = apply_mask(
                    [indep, low, high], nolims & everymask)
                for lh_masked in [lo_masked, hi_masked]:
                    # Since this has to work for x and y as dependent data, we
                    # first set both x and y to the independent variable and
                    # overwrite the respective dependent data in a second step.
                    line = mlines.Line2D(indep_masked, indep_masked,
                                         marker=marker, **eb_cap_style)
                    line.set(**{f"{dep_axis}data": lh_masked})
                    caplines.append(line)
            for idx, (lims, hl) in enumerate([(lolims, high), (uplims, low)]):
                if not lims.any():
                    continue
                hlmarker = (
                    himarker
                    if getattr(self, f"{dep_axis}axis").get_inverted() ^ idx
                    else lomarker)
                x_masked, y_masked, hl_masked = apply_mask(
                    [x, y, hl], lims & everymask)
                # As above, we set the dependent data in a second step.
                line = mlines.Line2D(x_masked, y_masked,
                                     marker=hlmarker, **eb_cap_style)
                line.set(**{f"{dep_axis}data": hl_masked})
                caplines.append(line)
                if capsize > 0:
                    caplines.append(mlines.Line2D(
                        x_masked, y_masked, marker=marker, **eb_cap_style))

        for l in caplines:
            self.add_line(l)

        self._request_autoscale_view()
        errorbar_container = ErrorbarContainer(
            (data_line, tuple(caplines), tuple(barcols)),
            has_xerr=(xerr is not None), has_yerr=(yerr is not None),
            label=label)
        self.containers.append(errorbar_container)

        return errorbar_container  # (l0, caplines, barcols)
