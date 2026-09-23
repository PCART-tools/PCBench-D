    @_api.make_keyword_only("3.9", "normed")
    @_preprocess_data(replace_names=["x", "y"], label_namer="y")
    def xcorr(self, x, y, normed=True, detrend=mlab.detrend_none,
              usevlines=True, maxlags=10, **kwargs):
        r"""
        Plot the cross correlation between *x* and *y*.

        The correlation with lag k is defined as
        :math:`\sum_n x[n+k] \cdot y^*[n]`, where :math:`y^*` is the complex
        conjugate of :math:`y`.

        Parameters
        ----------
        x, y : array-like of length n
            Neither *x* nor *y* are run through Matplotlib's unit conversion, so
            these should be unit-less arrays.

        detrend : callable, default: `.mlab.detrend_none` (no detrending)
            A detrending function applied to *x* and *y*.  It must have the
            signature ::

                detrend(x: np.ndarray) -> np.ndarray

        normed : bool, default: True
            If ``True``, input vectors are normalised to unit length.

        usevlines : bool, default: True
            Determines the plot style.

            If ``True``, vertical lines are plotted from 0 to the xcorr value
            using `.Axes.vlines`. Additionally, a horizontal line is plotted
            at y=0 using `.Axes.axhline`.

            If ``False``, markers are plotted at the xcorr values using
            `.Axes.plot`.

        maxlags : int, default: 10
            Number of lags to show. If None, will return all ``2 * len(x) - 1``
            lags.

        Returns
        -------
        lags : array (length ``2*maxlags+1``)
            The lag vector.
        c : array  (length ``2*maxlags+1``)
            The auto correlation vector.
        line : `.LineCollection` or `.Line2D`
            `.Artist` added to the Axes of the correlation:

            - `.LineCollection` if *usevlines* is True.
            - `.Line2D` if *usevlines* is False.
        b : `~matplotlib.lines.Line2D` or None
            Horizontal line at 0 if *usevlines* is True
            None *usevlines* is False.

        Other Parameters
        ----------------
        linestyle : `~matplotlib.lines.Line2D` property, optional
            The linestyle for plotting the data points.
            Only used if *usevlines* is ``False``.

        marker : str, default: 'o'
            The marker for plotting the data points.
            Only used if *usevlines* is ``False``.

        data : indexable object, optional
            DATA_PARAMETER_PLACEHOLDER

        **kwargs
            Additional parameters are passed to `.Axes.vlines` and
            `.Axes.axhline` if *usevlines* is ``True``; otherwise they are
            passed to `.Axes.plot`.

        Notes
        -----
        The cross correlation is performed with `numpy.correlate` with
        ``mode = "full"``.
        """
        Nx = len(x)
        if Nx != len(y):
            raise ValueError('x and y must be equal length')

        x = detrend(np.asarray(x))
        y = detrend(np.asarray(y))

        correls = np.correlate(x, y, mode="full")

        if normed:
            correls = correls / np.sqrt(np.dot(x, x) * np.dot(y, y))

        if maxlags is None:
            maxlags = Nx - 1

        if maxlags >= Nx or maxlags < 1:
            raise ValueError('maxlags must be None or strictly '
                             'positive < %d' % Nx)

        lags = np.arange(-maxlags, maxlags + 1)
        correls = correls[Nx - 1 - maxlags:Nx + maxlags]

        if usevlines:
            a = self.vlines(lags, [0], correls, **kwargs)
            # Make label empty so only vertical lines get a legend entry
            kwargs.pop('label', '')
            b = self.axhline(**kwargs)
        else:
            kwargs.setdefault('marker', 'o')
            kwargs.setdefault('linestyle', 'None')
            a, = self.plot(lags, correls, **kwargs)
            b = None
        return lags, correls, a, b
