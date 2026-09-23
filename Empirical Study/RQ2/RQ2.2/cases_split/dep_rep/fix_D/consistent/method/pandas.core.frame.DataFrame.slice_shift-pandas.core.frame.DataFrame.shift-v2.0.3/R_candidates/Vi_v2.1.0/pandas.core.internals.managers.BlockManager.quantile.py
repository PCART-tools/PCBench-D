    def quantile(
        self,
        *,
        qs: Index,  # with dtype float 64
        interpolation: QuantileInterpolation = "linear",
    ) -> Self:
        """
        Iterate over blocks applying quantile reduction.
        This routine is intended for reduction type operations and
        will do inference on the generated blocks.

        Parameters
        ----------
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

        new_axes = list(self.axes)
        new_axes[1] = Index(qs, dtype=np.float64)

        blocks = [
            blk.quantile(qs=qs, interpolation=interpolation) for blk in self.blocks
        ]

        return type(self)(blocks, new_axes)
