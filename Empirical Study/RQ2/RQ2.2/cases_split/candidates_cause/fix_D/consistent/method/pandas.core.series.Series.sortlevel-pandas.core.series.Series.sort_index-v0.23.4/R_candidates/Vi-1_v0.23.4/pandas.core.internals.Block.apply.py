    def apply(self, func, mgr=None, **kwargs):
        """ apply the function to my values; return a block if we are not
        one
        """
        with np.errstate(all='ignore'):
            result = func(self.values, **kwargs)
        if not isinstance(result, Block):
            result = self.make_block(values=_block_shape(result,
                                                         ndim=self.ndim))

        return result
