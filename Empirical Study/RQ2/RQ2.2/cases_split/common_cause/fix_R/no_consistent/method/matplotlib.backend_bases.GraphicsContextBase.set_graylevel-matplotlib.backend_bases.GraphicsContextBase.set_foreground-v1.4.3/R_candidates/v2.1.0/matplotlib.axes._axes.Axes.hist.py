    @_preprocess_data(replace_names=["x", 'weights'], label_namer="x")
    def hist(self, x, bins=None, range=None, density=None, weights=None,
             cumulative=False, bottom=None, histtype='bar', align='mid',
             orientation='vertical', rwidth=None, log=False,
             color=None, label=None, stacked=False, normed=None,
             **kwargs):
        """
        Plot a histogram.

        Compute and draw the histogram of *x*. The return value is a
        tuple (*n*, *bins*, *patches*) or ([*n0*, *n1*, ...], *bins*,
        [*patches0*, *patches1*,...]) if the input contains multiple
        data.

        Multiple data can be provided via *x* as a list of datasets
        of potentially different length ([*x0*, *x1*, ...]), or as
        a 2-D ndarray in which each column is a dataset.  Note that
        the ndarray form is transposed relative to the list form.

        Masked arrays are not supported at present.

        Parameters
        ----------
        x : (n,) array or sequence of (n,) arrays
            Input values, this takes either a single array or a sequency of
            arrays which are not required to be of the same length

        bins : integer or array_like or 'auto', optional
            If an integer is given, ``bins + 1`` bin edges are returned,
            consistently with :func:`numpy.histogram` for numpy version >=
            1.3.

            Unequally spaced bins are supported if *bins* is a sequence.

            If Numpy 1.11 is installed, may also be ``'auto'``.

            Default is taken from the rcParam ``hist.bins``.

        range : tuple or None, optional
            The lower and upper range of the bins. Lower and upper outliers
            are ignored. If not provided, *range* is ``(x.min(), x.max())``.
            Range has no effect if *bins* is a sequence.

            If *bins* is a sequence or *range* is specified, autoscaling
            is based on the specified bin range instead of the
            range of x.

            Default is ``None``

        density : boolean, optional
            If ``True``, the first element of the return tuple will
            be the counts normalized to form a probability density, i.e.,
            the area (or integral) under the histogram will sum to 1.
            This is achieved by dividing the count by the number of
            observations times the bin width and not dividing by the total
            number of observations. If *stacked* is also ``True``, the sum of
            the histograms is normalized to 1.

            Default is ``None`` for both *normed* and *density*. If either is
            set, then that value will be used. If neither are set, then the
            args will be treated as ``False``.

            If both *density* and *normed* are set an error is raised.

        weights : (n, ) array_like or None, optional
            An array of weights, of the same shape as *x*.  Each value in *x*
            only contributes its associated weight towards the bin count
            (instead of 1).  If *normed* or *density* is ``True``,
            the weights are normalized, so that the integral of the density
            over the range remains 1.

            Default is ``None``

        cumulative : boolean, optional
            If ``True``, then a histogram is computed where each bin gives the
            counts in that bin plus all bins for smaller values. The last bin
            gives the total number of datapoints. If *normed* or *density*
            is also ``True`` then the histogram is normalized such that the
            last bin equals 1. If *cumulative* evaluates to less than 0
            (e.g., -1), the direction of accumulation is reversed.
            In this case, if *normed* and/or *density* is also ``True``, then
            the histogram is normalized such that the first bin equals 1.

            Default is ``False``

        bottom : array_like, scalar, or None
            Location of the bottom baseline of each bin.  If a scalar,
            the base line for each bin is shifted by the same amount.
            If an array, each bin is shifted independently and the length
            of bottom must match the number of bins.  If None, defaults to 0.

            Default is ``None``

        histtype : {'bar', 'barstacked', 'step',  'stepfilled'}, optional
            The type of histogram to draw.

            - 'bar' is a traditional bar-type histogram.  If multiple data
              are given the bars are aranged side by side.

            - 'barstacked' is a bar-type histogram where multiple
              data are stacked on top of each other.

            - 'step' generates a lineplot that is by default
              unfilled.

            - 'stepfilled' generates a lineplot that is by default
              filled.

            Default is 'bar'

        align : {'left', 'mid', 'right'}, optional
            Controls how the histogram is plotted.

                - 'left': bars are centered on the left bin edges.

                - 'mid': bars are centered between the bin edges.

                - 'right': bars are centered on the right bin edges.

            Default is 'mid'

        orientation : {'horizontal', 'vertical'}, optional
            If 'horizontal', `~matplotlib.pyplot.barh` will be used for
            bar-type histograms and the *bottom* kwarg will be the left edges.

        rwidth : scalar or None, optional
            The relative width of the bars as a fraction of the bin width.  If
            ``None``, automatically compute the width.

            Ignored if *histtype* is 'step' or 'stepfilled'.

            Default is ``None``

        log : boolean, optional
            If ``True``, the histogram axis will be set to a log scale. If
            *log* is ``True`` and *x* is a 1D array, empty bins will be
            filtered out and only the non-empty ``(n, bins, patches)``
            will be returned.

            Default is ``False``

        color : color or array_like of colors or None, optional
            Color spec or sequence of color specs, one per dataset.  Default
            (``None``) uses the standard line color sequence.

            Default is ``None``

        label : string or None, optional
            String, or sequence of strings to match multiple datasets.  Bar
            charts yield multiple patches per dataset, but only the first gets
            the label, so that the legend command will work as expected.

            default is ``None``

        stacked : boolean, optional
            If ``True``, multiple data are stacked on top of each other If
            ``False`` multiple data are aranged side by side if histtype is
            'bar' or on top of each other if histtype is 'step'

            Default is ``False``

        Returns
        -------
        n : array or list of arrays
            The values of the histogram bins. See *normed* or *density*
            and *weights* for a description of the possible semantics.
            If input *x* is an array, then this is an array of length
            *nbins*. If input is a sequence arrays
            ``[data1, data2,..]``, then this is a list of arrays with
            the values of the histograms for each of the arrays in the
            same order.

        bins : array
            The edges of the bins. Length nbins + 1 (nbins left edges and right
            edge of last bin).  Always a single array even when multiple data
            sets are passed in.

        patches : list or list of lists
            Silent list of individual patches used to create the histogram
            or list of such list if multiple input datasets.

        Other Parameters
        ----------------
        **kwargs : `~matplotlib.patches.Patch` properties

        See also
        --------
        hist2d : 2D histograms

        Notes
        -----
        Until numpy release 1.5, the underlying numpy histogram function was
        incorrect with ``normed=True`` if bin sizes were unequal.  MPL
        inherited that error. It is now corrected within MPL when using
        earlier numpy versions.

        """
        # Avoid shadowing the builtin.
        bin_range = range
        del range

        if not self._hold:
            self.cla()

        if np.isscalar(x):
            x = [x]

        if bins is None:
            bins = rcParams['hist.bins']

        # Validate string inputs here so we don't have to clutter
        # subsequent code.
        if histtype not in ['bar', 'barstacked', 'step', 'stepfilled']:
            raise ValueError("histtype %s is not recognized" % histtype)

        if align not in ['left', 'mid', 'right']:
            raise ValueError("align kwarg %s is not recognized" % align)

        if orientation not in ['horizontal', 'vertical']:
            raise ValueError(
                "orientation kwarg %s is not recognized" % orientation)

        if histtype == 'barstacked' and not stacked:
            stacked = True

        if density is not None and normed is not None:
            raise ValueError("kwargs 'density' and 'normed' cannot be used "
                             "simultaneously. "
                             "Please only use 'density', since 'normed'"
                             "will be deprecated.")

        # process the unit information
        self._process_unit_info(xdata=x, kwargs=kwargs)
        x = self.convert_xunits(x)
        if bin_range is not None:
            bin_range = self.convert_xunits(bin_range)

        # Check whether bins or range are given explicitly.
        binsgiven = (cbook.iterable(bins) or bin_range is not None)

        # basic input validation
        input_empty = np.size(x) == 0

        # Massage 'x' for processing.
        if input_empty:
            x = np.array([[]])
        else:
            x = cbook._reshape_2D(x, 'x')
        nx = len(x)  # number of datasets

        # We need to do to 'weights' what was done to 'x'
        if weights is not None:
            w = cbook._reshape_2D(weights, 'weights')
        else:
            w = [None]*nx

        if len(w) != nx:
            raise ValueError('weights should have the same shape as x')

        for xi, wi in zip(x, w):
            if wi is not None and len(wi) != len(xi):
                raise ValueError(
                    'weights should have the same shape as x')

        if color is None:
            color = [self._get_lines.get_next_color() for i in xrange(nx)]
        else:
            color = mcolors.to_rgba_array(color)
            if len(color) != nx:
                raise ValueError("color kwarg must have one color per dataset")

        # If bins are not specified either explicitly or via range,
        # we need to figure out the range required for all datasets,
        # and supply that to np.histogram.
        if not binsgiven and not input_empty:
            xmin = np.inf
            xmax = -np.inf
            for xi in x:
                if len(xi) > 0:
                    xmin = min(xmin, xi.min())
                    xmax = max(xmax, xi.max())
            bin_range = (xmin, xmax)
        density = bool(density) or bool(normed)
        if density and not stacked:
            hist_kwargs = dict(range=bin_range, density=density)
        else:
            hist_kwargs = dict(range=bin_range)

        n = []
        mlast = None
        for i in xrange(nx):
            # this will automatically overwrite bins,
            # so that each histogram uses the same bins
            m, bins = np.histogram(x[i], bins, weights=w[i], **hist_kwargs)
            m = m.astype(float)  # causes problems later if it's an int
            if mlast is None:
                mlast = np.zeros(len(bins)-1, m.dtype)
            if density and not stacked:
                db = np.diff(bins)
                m = (m.astype(float) / db) / m.sum()
            if stacked:
                if mlast is None:
                    mlast = np.zeros(len(bins)-1, m.dtype)
                m += mlast
                mlast[:] = m
            n.append(m)

        if stacked and density:
            db = np.diff(bins)
            for m in n:
                m[:] = (m.astype(float) / db) / n[-1].sum()
        if cumulative:
            slc = slice(None)
            if cbook.is_numlike(cumulative) and cumulative < 0:
                slc = slice(None, None, -1)

            if density:
                n = [(m * np.diff(bins))[slc].cumsum()[slc] for m in n]
            else:
                n = [m[slc].cumsum()[slc] for m in n]

        patches = []

        # Save autoscale state for later restoration; turn autoscaling
        # off so we can do it all a single time at the end, instead
        # of having it done by bar or fill and then having to be redone.
        _saved_autoscalex = self.get_autoscalex_on()
        _saved_autoscaley = self.get_autoscaley_on()
        self.set_autoscalex_on(False)
        self.set_autoscaley_on(False)

        if histtype.startswith('bar'):

            totwidth = np.diff(bins)

            if rwidth is not None:
                dr = np.clip(rwidth, 0, 1)
            elif (len(n) > 1 and
                  ((not stacked) or rcParams['_internal.classic_mode'])):
                dr = 0.8
            else:
                dr = 1.0

            if histtype == 'bar' and not stacked:
                width = dr * totwidth / nx
                dw = width
                boffset = -0.5 * dr * totwidth * (1 - 1 / nx)
            elif histtype == 'barstacked' or stacked:
                width = dr * totwidth
                boffset, dw = 0.0, 0.0

            if align == 'mid' or align == 'edge':
                boffset += 0.5 * totwidth
            elif align == 'right':
                boffset += totwidth

            if orientation == 'horizontal':
                _barfunc = self.barh
                bottom_kwarg = 'left'
            else:  # orientation == 'vertical'
                _barfunc = self.bar
                bottom_kwarg = 'bottom'

            for m, c in zip(n, color):
                if bottom is None:
                    bottom = np.zeros(len(m))
                if stacked:
                    height = m - bottom
                else:
                    height = m
                patch = _barfunc(bins[:-1]+boffset, height, width,
                                 align='center', log=log,
                                 color=c, **{bottom_kwarg: bottom})
                patches.append(patch)
                if stacked:
                    bottom[:] = m
                boffset += dw

        elif histtype.startswith('step'):
            # these define the perimeter of the polygon
            x = np.zeros(4 * len(bins) - 3)
            y = np.zeros(4 * len(bins) - 3)

            x[0:2*len(bins)-1:2], x[1:2*len(bins)-1:2] = bins, bins[:-1]
            x[2*len(bins)-1:] = x[1:2*len(bins)-1][::-1]

            if bottom is None:
                bottom = np.zeros(len(bins) - 1)

            y[1:2*len(bins)-1:2], y[2:2*len(bins):2] = bottom, bottom
            y[2*len(bins)-1:] = y[1:2*len(bins)-1][::-1]

            if log:
                if orientation == 'horizontal':
                    self.set_xscale('log', nonposx='clip')
                    logbase = self.xaxis._scale.base
                else:  # orientation == 'vertical'
                    self.set_yscale('log', nonposy='clip')
                    logbase = self.yaxis._scale.base

                # Setting a minimum of 0 results in problems for log plots
                if np.min(bottom) > 0:
                    minimum = np.min(bottom)
                elif density or weights is not None:
                    # For data that is normed to form a probability density,
                    # set to minimum data value / logbase
                    # (gives 1 full tick-label unit for the lowest filled bin)
                    ndata = np.array(n)
                    minimum = (np.min(ndata[ndata > 0])) / logbase
                else:
                    # For non-normed (density = False) data,
                    # set the min to 1 / log base,
                    # again so that there is 1 full tick-label unit
                    # for the lowest bin
                    minimum = 1.0 / logbase

                y[0], y[-1] = minimum, minimum
            else:
                minimum = 0

            if align == 'left' or align == 'center':
                x -= 0.5*(bins[1]-bins[0])
            elif align == 'right':
                x += 0.5*(bins[1]-bins[0])

            # If fill kwarg is set, it will be passed to the patch collection,
            # overriding this
            fill = (histtype == 'stepfilled')

            xvals, yvals = [], []
            for m in n:
                if stacked:
                    # starting point for drawing polygon
                    y[0] = y[1]
                    # top of the previous polygon becomes the bottom
                    y[2*len(bins)-1:] = y[1:2*len(bins)-1][::-1]
                # set the top of this polygon
                y[1:2*len(bins)-1:2], y[2:2*len(bins):2] = (m + bottom,
                                                            m + bottom)
                if log:
                    y[y < minimum] = minimum
                if orientation == 'horizontal':
                    xvals.append(y.copy())
                    yvals.append(x.copy())
                else:
                    xvals.append(x.copy())
                    yvals.append(y.copy())

            # stepfill is closed, step is not
            split = -1 if fill else 2 * len(bins)
            # add patches in reverse order so that when stacking,
            # items lower in the stack are plotted on top of
            # items higher in the stack
            for x, y, c in reversed(list(zip(xvals, yvals, color))):
                patches.append(self.fill(
                    x[:split], y[:split],
                    closed=True if fill else None,
                    facecolor=c,
                    edgecolor=None if fill else c,
                    fill=fill if fill else None))
            for patch_list in patches:
                for patch in patch_list:
                    if orientation == 'vertical':
                        patch.sticky_edges.y.append(minimum)
                    elif orientation == 'horizontal':
                        patch.sticky_edges.x.append(minimum)

            # we return patches, so put it back in the expected order
            patches.reverse()

        self.set_autoscalex_on(_saved_autoscalex)
        self.set_autoscaley_on(_saved_autoscaley)
        self.autoscale_view()

        if label is None:
            labels = [None]
        elif isinstance(label, six.string_types):
            labels = [label]
        else:
            labels = [six.text_type(lab) for lab in label]

        for patch, lbl in zip_longest(patches, labels, fillvalue=None):
            if patch:
                p = patch[0]
                p.update(kwargs)
                if lbl is not None:
                    p.set_label(lbl)

                for p in patch[1:]:
                    p.update(kwargs)
                    p.set_label('_nolegend_')

        if nx == 1:
            return n[0], bins, cbook.silent_list('Patch', patches[0])
        else:
            return n, bins, cbook.silent_list('Lists of Patches', patches)
