    def _maybe_drop_cross_column(
        self, result: DataFrame, cross_col: str | None
    ) -> None:
        if cross_col is not None:
            del result[cross_col]
