    @_preprocess_data(replace_names=["x", "y"], label_namer="y")
    def xcorr(self, x, y, normed=True, detrend=mlab.detrend_none,
              usevlines=True, maxlags=10, **kwargs):
        """
        Plot the cross correlation between *x* and *y*.

        The correlation with lag k is defined as sum_n x[n+k] * conj(y[n]).

        Parameters
        ----------

        x : sequence of scalars of length n

        y : sequence of scalars of length n

        hold : boolean, optional, *deprecated*, default: True

        detrend : callable, optional, default: `mlab.detrend_none`
            x is detrended by the `detrend` callable. Default is no
            normalization.

        normed : boolean, optional, default: True
            if True, input vectors are normalised to unit length.

        usevlines : boolean, optional, default: True
            if True, Axes.vlines is used to plot the vertical lines from the
            origin to the acorr. Otherwise, Axes.plot is used.

        maxlags : integer, optional, default: 10
            number of lags to show. If None, will return all 2 * len(x) - 1
            lags.

        Returns
        -------
        (lags, c, line, b) : where:

          - `lags` are a length 2`maxlags+1 lag vector.
          - `c` is the 2`maxlags+1 auto correlation vectorI
          - `line` is a `~matplotlib.lines.Line2D` instance returned by
            `plot`.
          - `b` is the x-axis (none, if plot is used).

        Other Parameters
        ----------------
        linestyle : `~matplotlib.lines.Line2D` prop, optional, default: None
            Only used if usevlines is False.

        marker : string, optional, default: 'o'

        Notes
        -----
        The cross correlation is performed with :func:`numpy.correlate` with
        `mode` = 2.
        """
        if "hold" in kwargs:
            warnings.warn("the 'hold' kwarg is deprecated", mplDeprecation)

        Nx = len(x)
        if Nx != len(y):
            raise ValueError('x and y must be equal length')

        x = detrend(np.asarray(x))
        y = detrend(np.asarray(y))

        c = np.correlate(x, y, mode=2)

        if normed:
            c /= np.sqrt(np.dot(x, x) * np.dot(y, y))

        if maxlags is None:
            maxlags = Nx - 1

        if maxlags >= Nx or maxlags < 1:
            raise ValueError('maxlags must be None or strictly '
                             'positive < %d' % Nx)

        lags = np.arange(-maxlags, maxlags + 1)
        c = c[Nx - 1 - maxlags:Nx + maxlags]

        if usevlines:
            a = self.vlines(lags, [0], c, **kwargs)
            b = self.axhline(**kwargs)
        else:

            kwargs.setdefault('marker', 'o')
            kwargs.setdefault('linestyle', 'None')
            a, = self.plot(lags, c, **kwargs)
            b = None
        return lags, c, a, b
