    def apply(self, f, filter=None, **kwargs):
        """
        Iterate over the blocks, collect and create a new BlockManager.

        Parameters
        ----------
        f : str or callable
            Name of the Block method to apply.
        filter : list, if supplied, only call the block if the filter is in
                 the block

        Returns
        -------
        BlockManager
        """

        result_blocks = []

        # filter kwarg is used in replace-* family of methods
        if filter is not None:
            filter_locs = set(self.items.get_indexer_for(filter))
            if len(filter_locs) == len(self.items):
                # All items are included, as if there were no filtering
                filter = None
            else:
                kwargs["filter"] = filter_locs

        self._consolidate_inplace()

        if f == "where":
            align_copy = True
            if kwargs.get("align", True):
                align_keys = ["other", "cond"]
            else:
                align_keys = ["cond"]
        elif f == "putmask":
            align_copy = False
            if kwargs.get("align", True):
                align_keys = ["new", "mask"]
            else:
                align_keys = ["mask"]
        elif f == "fillna":
            # fillna internally does putmask, maybe it's better to do this
            # at mgr, not block level?
            align_copy = False
            align_keys = ["value"]
        else:
            align_keys = []

        # TODO(EA): may interfere with ExtensionBlock.setitem for blocks
        # with a .values attribute.
        aligned_args = {
            k: kwargs[k]
            for k in align_keys
            if not isinstance(kwargs[k], ABCExtensionArray)
            and hasattr(kwargs[k], "values")
        }

        for b in self.blocks:
            if filter is not None:
                if not b.mgr_locs.isin(filter_locs).any():
                    result_blocks.append(b)
                    continue

            if aligned_args:
                b_items = self.items[b.mgr_locs.indexer]

                for k, obj in aligned_args.items():
                    axis = obj._info_axis_number
                    kwargs[k] = obj.reindex(b_items, axis=axis, copy=align_copy)

            if callable(f):
                applied = b.apply(f, **kwargs)
            else:
                applied = getattr(b, f)(**kwargs)
            result_blocks = _extend_blocks(applied, result_blocks)

        if len(result_blocks) == 0:
            return self.make_empty(self.axes)
        bm = type(self)(result_blocks, self.axes, do_integrity_check=False)
        return bm
