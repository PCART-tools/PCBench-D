    @property
    def is_truncated_horizontally(self) -> bool:
        return bool(self.max_cols_fitted and (len(self.columns) > self.max_cols_fitted))
