    def apply(self, f, axes=None, filter=None, do_integrity_check=False, **kwargs):
        """
        iterate over the blocks, collect and create a new block manager

        Parameters
        ----------
        f : the callable or function name to operate on at the block level
        axes : optional (if not supplied, use self.axes)
        filter : list, if supplied, only call the block if the filter is in
                 the block
        do_integrity_check : boolean, default False. Do the block manager integrity check

        Returns
        -------
        Block Manager (new object)

        """

        result_blocks = []

        # filter kwarg is used in replace-* family of methods
        if filter is not None:
            filter_locs = set(self.items.get_indexer_for(filter))
            if len(filter_locs) == len(self.items):
                # All items are included, as if there were no filtering
                filter = None
            else:
                kwargs['filter'] = filter_locs

        if f == 'where' and kwargs.get('align', True):
            align_copy = True
            align_keys = ['other', 'cond']
        elif f == 'putmask' and kwargs.get('align', True):
            align_copy = False
            align_keys = ['new', 'mask']
        elif f == 'eval':
            align_copy = False
            align_keys = ['other']
        elif f == 'fillna':
            # fillna internally does putmask, maybe it's better to do this
            # at mgr, not block level?
            align_copy = False
            align_keys = ['value']
        else:
            align_keys = []

        aligned_args = dict((k, kwargs[k]) for k in align_keys
                            if hasattr(kwargs[k], 'reindex_axis'))

        for b in self.blocks:
            if filter is not None:
                if not b.mgr_locs.isin(filter_locs).any():
                    result_blocks.append(b)
                    continue

            if aligned_args:
                b_items = self.items[b.mgr_locs.indexer]

                for k, obj in aligned_args.items():
                    axis = getattr(obj, '_info_axis_number', 0)
                    kwargs[k] = obj.reindex_axis(b_items, axis=axis,
                                                 copy=align_copy)

            applied = getattr(b, f)(**kwargs)

            if isinstance(applied, list):
                result_blocks.extend(applied)
            else:
                result_blocks.append(applied)

        if len(result_blocks) == 0:
            return self.make_empty(axes or self.axes)
        bm = self.__class__(result_blocks, axes or self.axes,
                            do_integrity_check=do_integrity_check)
        bm._consolidate_inplace()
        return bm
