    def reduce(self, func, *args, **kwargs):
        # If 2D, we assume that we're operating column-wise
        if self.ndim == 1:
            # we'll be returning a scalar
            blk = self.blocks[0]
            return func(blk.values, *args, **kwargs)

        res = {}
        for blk in self.blocks:
            bres = func(blk.values, *args, **kwargs)

            if np.ndim(bres) == 0:
                # EA
                assert blk.shape[0] == 1
                new_res = zip(blk.mgr_locs.as_array, [bres])
            else:
                assert bres.ndim == 1, bres.shape
                assert blk.shape[0] == len(bres), (blk.shape, bres.shape, args, kwargs)
                new_res = zip(blk.mgr_locs.as_array, bres)

            nr = dict(new_res)
            assert not any(key in res for key in nr)
            res.update(nr)

        return res
