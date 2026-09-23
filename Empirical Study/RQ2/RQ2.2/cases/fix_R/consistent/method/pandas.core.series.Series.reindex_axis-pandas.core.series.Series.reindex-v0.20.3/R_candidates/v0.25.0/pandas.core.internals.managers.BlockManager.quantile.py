    def quantile(
        self,
        axis=0,
        consolidate=True,
        transposed=False,
        interpolation="linear",
        qs=None,
        numeric_only=None,
    ):
        """
        Iterate over blocks applying quantile reduction.
        This routine is intended for reduction type operations and
        will do inference on the generated blocks.

        Parameters
        ----------
        axis: reduction axis, default 0
        consolidate: boolean, default True. Join together blocks having same
            dtype
        transposed: boolean, default False
            we are holding transposed data
        interpolation : type of interpolation, default 'linear'
        qs : a scalar or list of the quantiles to be computed
        numeric_only : ignored

        Returns
        -------
        Block Manager (new object)
        """

        # Series dispatches to DataFrame for quantile, which allows us to
        #  simplify some of the code here and in the blocks
        assert self.ndim >= 2

        if consolidate:
            self._consolidate_inplace()

        def get_axe(block, qs, axes):
            # Because Series dispatches to DataFrame, we will always have
            #  block.ndim == 2
            from pandas import Float64Index

            if is_list_like(qs):
                ax = Float64Index(qs)
            else:
                ax = axes[0]
            return ax

        axes, blocks = [], []
        for b in self.blocks:
            block = b.quantile(axis=axis, qs=qs, interpolation=interpolation)

            axe = get_axe(b, qs, axes=self.axes)

            axes.append(axe)
            blocks.append(block)

        # note that some DatetimeTZ, Categorical are always ndim==1
        ndim = {b.ndim for b in blocks}
        assert 0 not in ndim, ndim

        if 2 in ndim:

            new_axes = list(self.axes)

            # multiple blocks that are reduced
            if len(blocks) > 1:
                new_axes[1] = axes[0]

                # reset the placement to the original
                for b, sb in zip(blocks, self.blocks):
                    b.mgr_locs = sb.mgr_locs

            else:
                new_axes[axis] = Index(np.concatenate([ax.values for ax in axes]))

            if transposed:
                new_axes = new_axes[::-1]
                blocks = [
                    b.make_block(b.values.T, placement=np.arange(b.shape[1]))
                    for b in blocks
                ]

            return self.__class__(blocks, new_axes)

        # single block, i.e. ndim == {1}
        values = _concat._concat_compat([b.values for b in blocks])

        # compute the orderings of our original data
        if len(self.blocks) > 1:

            indexer = np.empty(len(self.axes[0]), dtype=np.intp)
            i = 0
            for b in self.blocks:
                for j in b.mgr_locs:
                    indexer[j] = i
                    i = i + 1

            values = values.take(indexer)

        return SingleBlockManager(
            [make_block(values, ndim=1, placement=np.arange(len(values)))], axes[0]
        )
