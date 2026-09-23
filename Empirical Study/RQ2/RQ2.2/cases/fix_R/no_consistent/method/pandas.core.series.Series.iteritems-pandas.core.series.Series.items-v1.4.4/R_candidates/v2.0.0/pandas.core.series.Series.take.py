    @Appender(NDFrame.take.__doc__)
    def take(self, indices, axis: Axis = 0, **kwargs) -> Series:
        nv.validate_take((), kwargs)

        indices = ensure_platform_int(indices)

        if (
            indices.ndim == 1
            and using_copy_on_write()
            and is_range_indexer(indices, len(self))
        ):
            return self.copy(deep=None)

        new_index = self.index.take(indices)
        new_values = self._values.take(indices)

        result = self._constructor(new_values, index=new_index, fastpath=True)
        return result.__finalize__(self, method="take")
