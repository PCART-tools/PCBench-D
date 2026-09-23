    @_preprocess_data(replace_names=["x"], label_namer="x")
    def acorr(self, x, **kwargs):
        """
        Plot the autocorrelation of `x`.

        Parameters
        ----------

        x : sequence of scalar

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
          - `b` is the x-axis.

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
        return self.xcorr(x, x, **kwargs)
