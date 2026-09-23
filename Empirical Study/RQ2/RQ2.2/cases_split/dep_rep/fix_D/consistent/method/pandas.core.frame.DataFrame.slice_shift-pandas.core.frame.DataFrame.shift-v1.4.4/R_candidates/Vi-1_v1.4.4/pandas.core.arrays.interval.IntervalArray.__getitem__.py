    def __getitem__(
        self: IntervalArrayT, key: PositionalIndexer
    ) -> IntervalArrayT | IntervalOrNA:
        key = check_array_indexer(self, key)
        left = self._left[key]
        right = self._right[key]

        if not isinstance(left, (np.ndarray, ExtensionArray)):
            # scalar
            if is_scalar(left) and isna(left):
                return self._fill_value
            return Interval(left, right, self.closed)
        # error: Argument 1 to "ndim" has incompatible type "Union[ndarray,
        # ExtensionArray]"; expected "Union[Union[int, float, complex, str, bytes,
        # generic], Sequence[Union[int, float, complex, str, bytes, generic]],
        # Sequence[Sequence[Any]], _SupportsArray]"
        if np.ndim(left) > 1:  # type: ignore[arg-type]
            # GH#30588 multi-dimensional indexer disallowed
            raise ValueError("multi-dimensional indexing not allowed")
        return self._shallow_copy(left, right)
