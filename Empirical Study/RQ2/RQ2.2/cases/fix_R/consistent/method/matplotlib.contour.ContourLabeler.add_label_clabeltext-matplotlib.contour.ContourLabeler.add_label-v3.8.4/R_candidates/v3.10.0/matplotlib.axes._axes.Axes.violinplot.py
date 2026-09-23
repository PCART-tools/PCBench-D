    @_api.make_keyword_only("3.9", "vert")
    @_preprocess_data(replace_names=["dataset"])
    def violinplot(self, dataset, positions=None, vert=None,
                   orientation='vertical', widths=0.5, showmeans=False,
                   showextrema=True, showmedians=False, quantiles=None,
                   points=100, bw_method=None, side='both',):
        """
        Make a violin plot.

        Make a violin plot for each column of *dataset* or each vector in
        sequence *dataset*.  Each filled area extends to represent the
        entire data range, with optional lines at the mean, the median,
        the minimum, the maximum, and user-specified quantiles.

        Parameters
        ----------
        dataset : Array or a sequence of vectors.
            The input data.

        positions : array-like, default: [1, 2, ..., n]
            The positions of the violins; i.e. coordinates on the x-axis for
            vertical violins (or y-axis for horizontal violins).

        vert : bool, optional
            .. deprecated:: 3.10
                Use *orientation* instead.

                If this is given during the deprecation period, it overrides
                the *orientation* parameter.

            If True, plots the violins vertically.
            If False, plots the violins horizontally.

        orientation : {'vertical', 'horizontal'}, default: 'vertical'
            If 'horizontal', plots the violins horizontally.
            Otherwise, plots the violins vertically.

            .. versionadded:: 3.10

        widths : float or array-like, default: 0.5
            The maximum width of each violin in units of the *positions* axis.
            The default is 0.5, which is half the available space when using default
            *positions*.

        showmeans : bool, default: False
            Whether to show the mean with a line.

        showextrema : bool, default: True
            Whether to show extrema with a line.

        showmedians : bool, default: False
            Whether to show the median with a line.

        quantiles : array-like, default: None
            If not None, set a list of floats in interval [0, 1] for each violin,
            which stands for the quantiles that will be rendered for that
            violin.

        points : int, default: 100
            The number of points to evaluate each of the gaussian kernel density
            estimations at.

        bw_method : {'scott', 'silverman'} or float or callable, default: 'scott'
            The method used to calculate the estimator bandwidth.  If a
            float, this will be used directly as `kde.factor`.  If a
            callable, it should take a `matplotlib.mlab.GaussianKDE` instance as
            its only parameter and return a float.

        side : {'both', 'low', 'high'}, default: 'both'
            'both' plots standard violins. 'low'/'high' only
            plots the side below/above the positions value.

        data : indexable object, optional
            DATA_PARAMETER_PLACEHOLDER

        Returns
        -------
        dict
            A dictionary mapping each component of the violinplot to a
            list of the corresponding collection instances created. The
            dictionary has the following keys:

            - ``bodies``: A list of the `~.collections.PolyCollection`
              instances containing the filled area of each violin.

            - ``cmeans``: A `~.collections.LineCollection` instance that marks
              the mean values of each of the violin's distribution.

            - ``cmins``: A `~.collections.LineCollection` instance that marks
              the bottom of each violin's distribution.

            - ``cmaxes``: A `~.collections.LineCollection` instance that marks
              the top of each violin's distribution.

            - ``cbars``: A `~.collections.LineCollection` instance that marks
              the centers of each violin's distribution.

            - ``cmedians``: A `~.collections.LineCollection` instance that
              marks the median values of each of the violin's distribution.

            - ``cquantiles``: A `~.collections.LineCollection` instance created
              to identify the quantile values of each of the violin's
              distribution.

        See Also
        --------
        .Axes.violin : Draw a violin from pre-computed statistics.
        boxplot : Draw a box and whisker plot.
        """

        def _kde_method(X, coords):
            # Unpack in case of e.g. Pandas or xarray object
            X = cbook._unpack_to_numpy(X)
            # fallback gracefully if the vector contains only one value
            if np.all(X[0] == X):
                return (X[0] == coords).astype(float)
            kde = mlab.GaussianKDE(X, bw_method)
            return kde.evaluate(coords)

        vpstats = cbook.violin_stats(dataset, _kde_method, points=points,
                                     quantiles=quantiles)
        return self.violin(vpstats, positions=positions, vert=vert,
                           orientation=orientation, widths=widths,
                           showmeans=showmeans, showextrema=showextrema,
                           showmedians=showmedians, side=side)
