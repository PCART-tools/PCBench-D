    def make_block_same_class(self, values, placement=None, ndim=None, dtype=None):
        """ Wrap given values in a block of same type as self. """
        if dtype is not None:
            # issue 19431 fastparquet is passing this
            warnings.warn(
                "dtype argument is deprecated, will be removed in a future release.",
                FutureWarning,
            )
        if placement is None:
            placement = self.mgr_locs
        return make_block(
            values, placement=placement, ndim=ndim, klass=self.__class__, dtype=dtype
        )
