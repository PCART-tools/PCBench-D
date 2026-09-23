    @_preprocess_data(replace_names=["x", "weights"], label_namer="x")
    @_docstring.interpd
    def ecdf(self, x, weights=None, *, complementary=False,
             orientation="vertical", compress=False, **kwargs):
        """
        Compute and plot the empirical cumulative distribution function of *x*.

        .. versionadded:: 3.8

        Parameters
        ----------
        x : 1d array-like
            The input data.  Infinite entries are kept (and move the relevant
            end of the ecdf from 0/1), but NaNs and masked values are errors.

        weights : 1d array-like or None, default: None
            The weights of the entries; must have the same shape as *x*.
            Weights corresponding to NaN data points are dropped, and then the
            remaining weights are normalized to sum to 1.  If unset, all
            entries have the same weight.

        complementary : bool, default: False
            Whether to plot a cumulative distribution function, which increases
            from 0 to 1 (the default), or a complementary cumulative
            distribution function, which decreases from 1 to 0.

        orientation : {"vertical", "horizontal"}, default: "vertical"
            Whether the entries are plotted along the x-axis ("vertical", the
            default) or the y-axis ("horizontal").  This parameter takes the
            same values as in `~.Axes.hist`.

        compress : bool, default: False
            Whether multiple entries with the same values are grouped together
            (with a summed weight) before plotting.  This is mainly useful if
            *x* contains many identical data points, to decrease the rendering
            complexity of the plot. If *x* contains no duplicate points, this
            has no effect and just uses some time and memory.

        Other Parameters
        ----------------
        data : indexable object, optional
            DATA_PARAMETER_PLACEHOLDER

        **kwargs
            Keyword arguments control the `.Line2D` properties:

            %(Line2D:kwdoc)s

        Returns
        -------
        `.Line2D`

        Notes
        -----
        The ecdf plot can be thought of as a cumulative histogram with one bin
        per data entry; i.e. it reports on the entire dataset without any
        arbitrary binning.

        If *x* contains NaNs or masked entries, either remove them first from
        the array (if they should not taken into account), or replace them by
        -inf or +inf (if they should be sorted at the beginning or the end of
        the array).
        """
        _api.check_in_list(["horizontal", "vertical"], orientation=orientation)
        if "drawstyle" in kwargs or "ds" in kwargs:
            raise TypeError("Cannot pass 'drawstyle' or 'ds' to ecdf()")
        if np.ma.getmask(x).any():
            raise ValueError("ecdf() does not support masked entries")
        x = np.asarray(x)
        if np.isnan(x).any():
            raise ValueError("ecdf() does not support NaNs")
        argsort = np.argsort(x)
        x = x[argsort]
        if weights is None:
            # Ensure that we end at exactly 1, avoiding floating point errors.
            cum_weights = (1 + np.arange(len(x))) / len(x)
        else:
            weights = np.take(weights, argsort)   # Reorder weights like we reordered x.
            cum_weights = np.cumsum(weights / np.sum(weights))
        if compress:
            # Get indices of unique x values.
            compress_idxs = [0, *(x[:-1] != x[1:]).nonzero()[0] + 1]
            x = x[compress_idxs]
            cum_weights = cum_weights[compress_idxs]
        if orientation == "vertical":
            if not complementary:
                line, = self.plot([x[0], *x], [0, *cum_weights],
                                  drawstyle="steps-post", **kwargs)
            else:
                line, = self.plot([*x, x[-1]], [1, *1 - cum_weights],
                                  drawstyle="steps-pre", **kwargs)
            line.sticky_edges.y[:] = [0, 1]
        else:  # orientation == "horizontal":
            if not complementary:
                line, = self.plot([0, *cum_weights], [x[0], *x],
                                  drawstyle="steps-pre", **kwargs)
            else:
                line, = self.plot([1, *1 - cum_weights], [*x, x[-1]],
                                  drawstyle="steps-post", **kwargs)
            line.sticky_edges.x[:] = [0, 1]
        return line
