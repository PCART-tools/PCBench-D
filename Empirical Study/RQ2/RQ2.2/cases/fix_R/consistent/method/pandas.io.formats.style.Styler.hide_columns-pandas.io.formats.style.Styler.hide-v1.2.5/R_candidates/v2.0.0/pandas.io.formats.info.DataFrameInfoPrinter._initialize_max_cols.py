    def _initialize_max_cols(self, max_cols: int | None) -> int:
        if max_cols is None:
            return get_option("display.max_info_columns", self.col_count + 1)
        return max_cols
