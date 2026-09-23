    def __getitem__(
        self,
        item: (int | Series | range | slice | np.ndarray[Any, Any] | list[int]),
    ) -> Any:
        if isinstance(item, Series) and item.dtype.is_integer():
            return self._take_with_series(item._pos_idxs(self.len()))

        elif _check_for_numpy(item) and isinstance(item, np.ndarray):
            return self._take_with_series(numpy_to_idxs(item, self.len()))

        # Integer
        elif isinstance(item, int):
            return self._s.get_index_signed(item)

        # Slice
        elif isinstance(item, slice):
            return PolarsSlice(self).apply(item)

        # Range
        elif isinstance(item, range):
            return self[range_to_slice(item)]

        # Sequence of integers (also triggers on empty sequence)
        elif isinstance(item, Sequence) and (
            not item or (isinstance(item[0], int) and not isinstance(item[0], bool))  # type: ignore[redundant-expr]
        ):
            idx_series = Series("", item, dtype=Int64)._pos_idxs(self.len())
            if idx_series.has_validity():
                msg = "cannot use `__getitem__` with index values containing nulls"
                raise ValueError(msg)
            return self._take_with_series(idx_series)

        msg = (
            f"cannot use `__getitem__` on Series of dtype {self.dtype!r}"
            f" with argument {item!r} of type {type(item).__name__!r}"
        )
        raise TypeError(msg)
