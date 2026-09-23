    @property
    def max_rows(self) -> int:
        """Maximum info rows to be displayed."""
        return get_option("display.max_info_rows", len(self.data) + 1)
