    def take(
        self, indices, axis: int = 0, allow_fill: bool = True, fill_value=None, **kwargs
    ) -> Int64Index:
        with rewrite_exception("Int64Index", type(self).__name__):
            return self._int64index.take(
                indices,
                axis=axis,
                allow_fill=allow_fill,
                fill_value=fill_value,
                **kwargs,
            )
