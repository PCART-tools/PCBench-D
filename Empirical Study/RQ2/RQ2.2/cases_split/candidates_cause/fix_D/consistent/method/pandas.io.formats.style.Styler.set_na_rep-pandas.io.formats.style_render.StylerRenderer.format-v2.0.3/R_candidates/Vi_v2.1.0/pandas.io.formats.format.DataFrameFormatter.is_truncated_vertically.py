    @property
    def is_truncated_vertically(self) -> bool:
        return bool(self.max_rows_fitted and (len(self.frame) > self.max_rows_fitted))
