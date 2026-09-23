    def _initialize_columns(self, columns: Sequence[Hashable] | None) -> Index:
        if columns is not None:
            # GH 47231 - columns doesn't have to be `Sequence[str]`
            # Will fix in later PR
            cols = ensure_index(cast(Axes, columns))
            self.frame = self.frame[cols]
            return cols
        else:
            return self.frame.columns
