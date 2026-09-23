    @maybe_split
    def reduce(self, func, ignore_failures: bool = False) -> list[Block]:
        """
        For object-dtype, we operate column-wise.
        """
        assert self.ndim == 2

        try:
            res = func(self.values)
        except TypeError:
            if not ignore_failures:
                raise
            return []

        assert isinstance(res, np.ndarray)
        assert res.ndim == 1
        res = res.reshape(1, -1)
        return [self.make_block_same_class(res)]
