    def quantile(
        self: T,
        *,
        qs: Index,  # with dtype float 64
        axis: AxisInt = 0,
        interpolation: QuantileInterpolation = "linear",
    ) -> T:
        """
        Iterate over blocks applying quantile reduction.
        This routine is intended for reduction type operations and
        will do inference on the generated blocks.

        Parameters
        ----------
        axis: reduction axis, default 0
        consolidate: bool, default True. Join together blocks having same
            dtype
        interpolation : type of interpolation, default 'linear'
        qs : list of the quantiles to be computed

        Returns
        -------
        BlockManager
        """
        # Series dispatches to DataFrame for quantile, which allows us to
        #  simplify some of the code here and in the blocks
        assert self.ndim >= 2
        assert is_list_like(qs)  # caller is responsible for this
        assert axis == 1  # only ever called this way

        new_axes = list(self.axes)
        new_axes[1] = Index(qs, dtype=np.float64)

        blocks = [
            blk.quantile(axis=axis, qs=qs, interpolation=interpolation)
            for blk in self.blocks
        ]

        return type(self)(blocks, new_axes)
