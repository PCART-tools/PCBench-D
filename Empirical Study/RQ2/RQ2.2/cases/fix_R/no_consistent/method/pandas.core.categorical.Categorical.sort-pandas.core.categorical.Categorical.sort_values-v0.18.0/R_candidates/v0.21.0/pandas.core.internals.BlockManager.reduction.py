    def reduction(self, f, axis=0, consolidate=True, transposed=False,
                  **kwargs):
        """
        iterate over the blocks, collect and create a new block manager.
        This routine is intended for reduction type operations and
        will do inference on the generated blocks.

        Parameters
        ----------
        f: the callable or function name to operate on at the block level
        axis: reduction axis, default 0
        consolidate: boolean, default True. Join together blocks having same
            dtype
        transposed: boolean, default False
            we are holding transposed data

        Returns
        -------
        Block Manager (new object)

        """

        if consolidate:
            self._consolidate_inplace()

        axes, blocks = [], []
        for b in self.blocks:
            kwargs['mgr'] = self
            axe, block = getattr(b, f)(axis=axis, **kwargs)

            axes.append(axe)
            blocks.append(block)

        # note that some DatetimeTZ, Categorical are always ndim==1
        ndim = set([b.ndim for b in blocks])

        if 2 in ndim:

            new_axes = list(self.axes)

            # multiple blocks that are reduced
            if len(blocks) > 1:
                new_axes[1] = axes[0]

                # reset the placement to the original
                for b, sb in zip(blocks, self.blocks):
                    b.mgr_locs = sb.mgr_locs

            else:
                new_axes[axis] = Index(np.concatenate(
                    [ax.values for ax in axes]))

            if transposed:
                new_axes = new_axes[::-1]
                blocks = [b.make_block(b.values.T,
                                       placement=np.arange(b.shape[1])
                                       ) for b in blocks]

            return self.__class__(blocks, new_axes)

        # 0 ndim
        if 0 in ndim and 1 not in ndim:
            values = np.array([b.values for b in blocks])
            if len(values) == 1:
                return values.item()
            blocks = [make_block(values, ndim=1)]
            axes = Index([ax[0] for ax in axes])

        # single block
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
            [make_block(values,
                        ndim=1,
                        placement=np.arange(len(values)))],
            axes[0])
