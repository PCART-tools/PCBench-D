    @final
    def __pos__(self):
        def blk_func(values: ArrayLike):
            if is_bool_dtype(values.dtype):
                return values.copy()
            else:
                return operator.pos(values)

        new_data = self._mgr.apply(blk_func)
        res = self._constructor(new_data)
        return res.__finalize__(self, method="__pos__")
