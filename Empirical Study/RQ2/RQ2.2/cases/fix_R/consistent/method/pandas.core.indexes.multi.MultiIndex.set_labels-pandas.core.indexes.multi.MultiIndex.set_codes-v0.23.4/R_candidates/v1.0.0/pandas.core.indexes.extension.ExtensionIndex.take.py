    @Appender(Index.take.__doc__)
    def take(self, indices, axis=0, allow_fill=True, fill_value=None, **kwargs):
        nv.validate_take(tuple(), kwargs)
        indices = ensure_platform_int(indices)

        taken = self._assert_take_fillable(
            self._data,
            indices,
            allow_fill=allow_fill,
            fill_value=fill_value,
            na_value=self._na_value,
        )
        return type(self)(taken, name=self.name)
