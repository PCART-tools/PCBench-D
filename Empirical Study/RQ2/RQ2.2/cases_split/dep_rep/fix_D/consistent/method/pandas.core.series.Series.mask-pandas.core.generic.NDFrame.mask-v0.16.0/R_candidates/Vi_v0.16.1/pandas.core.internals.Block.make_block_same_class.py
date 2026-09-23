    def make_block_same_class(self, values, placement, copy=False, fastpath=True,
                              **kwargs):
        """
        Wrap given values in a block of same type as self.

        `kwargs` are used in SparseBlock override.

        """
        if copy:
            values = values.copy()
        return make_block(values, placement, klass=self.__class__,
                          fastpath=fastpath, **kwargs)
