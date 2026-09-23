    def post_merge(self, objs, **kwargs):
        """ try to sparsify items that were previously sparse """
        is_sparse = defaultdict(list)
        for o in objs:
            for blk in o._data.blocks:
                if blk.is_sparse:

                    # record the dtype of each item
                    for i in blk.items:
                        is_sparse[i].append(blk.dtype)

        if len(is_sparse):
            return self.apply('post_merge', items=is_sparse)

        return self
