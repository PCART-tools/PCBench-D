    @_preprocess_data(replace_names=["x"], label_namer="x")
    def acorr(self, x, **kwargs):
        """
        Plot the autocorrelation of *x*.

        Parameters
        ----------
        x : array-like

        detrend : callable, default: `.mlab.detrend_none` (no detrending)
            A detrending function applied to *x*.  It must have the
            signature ::

                detrend(x: np.ndarray) -> np.ndarray

        normed : bool, default: True
            If ``True``, input vectors are normalised to unit length.

        usevlines : bool, default: True
            Determines the plot style.

            If ``True``, vertical lines are plotted from 0 to the acorr value
            using `.Axes.vlines`. Additionally, a horizontal line is plotted
            at y=0 using `.Axes.axhline`.

            If ``False``, markers are plotted at the acorr values using
            `.Axes.plot`.

        maxlags : int, default: 10
            Number of lags to show. If ``None``, will return all
            ``2 * len(x) - 1`` lags.

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
        b : `.Line2D` or None
            Horizontal line at 0 if *usevlines* is True
            None *usevlines* is False.

        Other Parameters
        ----------------
        linestyle : `.Line2D` property, optional
            The linestyle for plotting the data points.
            Only used if *usevlines* is ``False``.

        marker : str, default: 'o'
            The marker for plotting the data points.
            Only used if *usevlines* is ``False``.

        **kwargs
            Additional parameters are passed to `.Axes.vlines` and
            `.Axes.axhline` if *usevlines* is ``True``; otherwise they are
            passed to `.Axes.plot`.

        Notes
        -----
        The cross correlation is performed with `numpy.correlate` with
        ``mode = "full"``.
        """
        return self.xcorr(x, x, **kwargs)
