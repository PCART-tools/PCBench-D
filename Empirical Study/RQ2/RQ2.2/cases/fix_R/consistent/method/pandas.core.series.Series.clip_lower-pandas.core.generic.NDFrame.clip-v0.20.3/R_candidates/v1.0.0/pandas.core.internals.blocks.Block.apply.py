    def apply(self, func, **kwargs):
        """ apply the function to my values; return a block if we are not
        one
        """
        with np.errstate(all="ignore"):
            result = func(self.values, **kwargs)

        if is_extension_array_dtype(result) and result.ndim > 1:
            # if we get a 2D ExtensionArray, we need to split it into 1D pieces
            nbs = []
            for i, loc in enumerate(self.mgr_locs):
                vals = result[i]
                nv = _block_shape(vals, ndim=self.ndim)
                block = self.make_block(values=nv, placement=[loc])
                nbs.append(block)
            return nbs

        if not isinstance(result, Block):
            result = self.make_block(values=_block_shape(result, ndim=self.ndim))

        return result
