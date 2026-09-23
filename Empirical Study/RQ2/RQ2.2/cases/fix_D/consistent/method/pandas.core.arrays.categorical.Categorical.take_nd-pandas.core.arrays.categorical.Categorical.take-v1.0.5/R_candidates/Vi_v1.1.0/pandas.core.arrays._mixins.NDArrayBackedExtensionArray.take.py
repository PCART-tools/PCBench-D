    def take(
        self: _T,
        indices: Sequence[int],
        allow_fill: bool = False,
        fill_value: Any = None,
    ) -> _T:
        if allow_fill:
            fill_value = self._validate_fill_value(fill_value)

        new_data = take(
            self._ndarray, indices, allow_fill=allow_fill, fill_value=fill_value,
        )
        return self._from_backing_data(new_data)
