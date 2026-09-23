    @_preprocess_data(replace_names=["x"], label_namer="x")
    def acorr(self, x, **kwargs):
        """
        Plot the autocorrelation of *x*.

        Parameters
        ----------

        x : sequence of scalar

        detrend : callable, optional, default: `mlab.detrend_none`
            *x* is detrended by the *detrend* callable. Default is no
            normalization.

        normed : bool, optional, default: True
            If ``True``, input vectors are normalised to unit length.

        usevlines : bool, optional, default: True
            If ``True``, `Axes.vlines` is used to plot the vertical lines from
            the origin to the acorr. Otherwise, `Axes.plot` is used.

        maxlags : int, optional, default: 10
            Number of lags to show. If ``None``, will return all
            ``2 * len(x) - 1`` lags.

        Returns
        -------
        lags : array (length ``2*maxlags+1``)
            lag vector.
        c : array  (length ``2*maxlags+1``)
            auto correlation vector.
        line : `.LineCollection` or `.Line2D`
            `.Artist` added to the axes of the correlation.

             `.LineCollection` if *usevlines* is True
             `.Line2D` if *usevlines* is False
        b : `.Line2D` or None
            Horizontal line at 0 if *usevlines* is True
            None *usevlines* is False

        Other Parameters
        ----------------
        linestyle : `.Line2D` property, optional, default: None
            Only used if usevlines is ``False``.

        marker : str, optional, default: 'o'

        Notes
        -----
        The cross correlation is performed with :func:`numpy.correlate` with
        ``mode = 2``.
        """
        return self.xcorr(x, x, **kwargs)
