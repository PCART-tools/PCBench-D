    def apply(self, func, **kwargs):
        """ apply the function to my values; return a block if we are not one """
        result = func(self.values, **kwargs)
        if not isinstance(result, Block):
            result = make_block(values=_block_shape(result), placement=self.mgr_locs,)

        return result
