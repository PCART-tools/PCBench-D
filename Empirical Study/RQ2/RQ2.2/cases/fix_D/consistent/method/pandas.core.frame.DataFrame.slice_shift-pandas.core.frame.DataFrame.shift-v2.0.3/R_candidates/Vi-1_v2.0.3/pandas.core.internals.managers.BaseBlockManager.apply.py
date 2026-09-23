    def apply(
        self: T,
        f,
        align_keys: list[str] | None = None,
        **kwargs,
    ) -> T:
        """
        Iterate over the blocks, collect and create a new BlockManager.

        Parameters
        ----------
        f : str or callable
            Name of the Block method to apply.
        align_keys: List[str] or None, default None
        **kwargs
            Keywords to pass to `f`

        Returns
        -------
        BlockManager
        """
        assert "filter" not in kwargs

        align_keys = align_keys or []
        result_blocks: list[Block] = []
        # fillna: Series/DataFrame is responsible for making sure value is aligned

        aligned_args = {k: kwargs[k] for k in align_keys}

        for b in self.blocks:
            if aligned_args:
                for k, obj in aligned_args.items():
                    if isinstance(obj, (ABCSeries, ABCDataFrame)):
                        # The caller is responsible for ensuring that
                        #  obj.axes[-1].equals(self.items)
                        if obj.ndim == 1:
                            kwargs[k] = obj.iloc[b.mgr_locs.indexer]._values
                        else:
                            kwargs[k] = obj.iloc[:, b.mgr_locs.indexer]._values
                    else:
                        # otherwise we have an ndarray
                        kwargs[k] = obj[b.mgr_locs.indexer]

            if callable(f):
                applied = b.apply(f, **kwargs)
            else:
                applied = getattr(b, f)(**kwargs)
            result_blocks = extend_blocks(applied, result_blocks)

        out = type(self).from_blocks(result_blocks, self.axes)
        return out
