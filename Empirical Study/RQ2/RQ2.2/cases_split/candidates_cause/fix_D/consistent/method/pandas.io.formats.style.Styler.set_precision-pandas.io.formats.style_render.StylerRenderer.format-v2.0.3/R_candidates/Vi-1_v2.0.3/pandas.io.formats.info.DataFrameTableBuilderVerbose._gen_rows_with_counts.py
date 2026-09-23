    def _gen_rows_with_counts(self) -> Iterator[Sequence[str]]:
        """Iterator with string representation of body data with counts."""
        yield from zip(
            self._gen_line_numbers(),
            self._gen_columns(),
            self._gen_non_null_counts(),
            self._gen_dtypes(),
        )
