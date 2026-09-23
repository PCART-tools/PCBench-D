    def _initialize_show_counts(self, show_counts: bool | None) -> bool:
        if show_counts is None:
            return bool(not self.exceeds_info_cols and not self.exceeds_info_rows)
        else:
            return show_counts
