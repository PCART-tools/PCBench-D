    @property
    def _need_to_wrap_around(self) -> bool:
        return bool(self.fmt.max_cols is None or self.fmt.max_cols > 0)
