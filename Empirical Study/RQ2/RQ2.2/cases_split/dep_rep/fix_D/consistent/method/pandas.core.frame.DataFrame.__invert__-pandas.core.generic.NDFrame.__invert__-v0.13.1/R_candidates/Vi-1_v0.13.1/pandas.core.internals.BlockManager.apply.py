    def apply(self, f, *args, **kwargs):
        """ iterate over the blocks, collect and create a new block manager

        Parameters
        ----------
        f : the callable or function name to operate on at the block level
        axes : optional (if not supplied, use self.axes)
        filter : list, if supplied, only call the block if the filter is in
            the block
        """

        axes = kwargs.pop('axes', None)
        filter = kwargs.get('filter')
        do_integrity_check = kwargs.pop('do_integrity_check', False)
        result_blocks = []
        for blk in self.blocks:
            if filter is not None:
                kwargs['filter'] = set(kwargs['filter'])
                if not blk.items.isin(filter).any():
                    result_blocks.append(blk)
                    continue
            if callable(f):
                applied = f(blk, *args, **kwargs)

                # if we are no a block, try to coerce
                if not isinstance(applied, Block):
                    applied = make_block(applied,
                                         blk.items,
                                         blk.ref_items)

            else:
                applied = getattr(blk, f)(*args, **kwargs)

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
