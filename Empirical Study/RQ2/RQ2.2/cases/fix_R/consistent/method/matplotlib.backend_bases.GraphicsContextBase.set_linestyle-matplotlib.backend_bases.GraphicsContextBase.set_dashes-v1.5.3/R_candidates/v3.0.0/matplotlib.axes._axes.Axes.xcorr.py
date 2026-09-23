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
        x : sequence of scalars of length n

        y : sequence of scalars of length n

        detrend : callable, optional, default: `mlab.detrend_none`
            *x* is detrended by the *detrend* callable. Default is no
            normalization.

        normed : bool, optional, default: True
            If ``True``, input vectors are normalised to unit length.

        usevlines : bool, optional, default: True
            If ``True``, `Axes.vlines` is used to plot the vertical lines from
            the origin to the acorr. Otherwise, `Axes.plot` is used.

        maxlags : int, optional
            Number of lags to show. If None, will return all ``2 * len(x) - 1``
            lags. Default is 10.

        Returns
        -------
        lags : array (length ``2*maxlags+1``)
            lag vector.
        c : array  (length ``2*maxlags+1``)
            auto correlation vector.
        line : `.LineCollection` or `.Line2D`
            `.Artist` added to the axes of the correlation

             `.LineCollection` if *usevlines* is True
             `.Line2D` if *usevlines* is False
        b : `.Line2D` or None
            Horizontal line at 0 if *usevlines* is True
            None *usevlines* is False

        Other Parameters
        ----------------
        linestyle : `.Line2D` property, optional
            Only used if usevlines is ``False``.

        marker : string, optional
            Default is 'o'.

        Notes
        -----
        The cross correlation is performed with :func:`numpy.correlate` with
        ``mode = 2``.
        """
        Nx = len(x)
        if Nx != len(y):
            raise ValueError('x and y must be equal length')

        x = detrend(np.asarray(x))
        y = detrend(np.asarray(y))

        correls = np.correlate(x, y, mode=2)

        if normed:
            correls /= np.sqrt(np.dot(x, x) * np.dot(y, y))

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
