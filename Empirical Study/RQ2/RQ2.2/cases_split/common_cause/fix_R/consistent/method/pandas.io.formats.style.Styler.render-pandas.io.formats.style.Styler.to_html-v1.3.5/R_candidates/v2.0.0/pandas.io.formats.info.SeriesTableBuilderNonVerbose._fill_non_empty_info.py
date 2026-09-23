    def _fill_non_empty_info(self) -> None:
        """Add lines to the info table, pertaining to non-empty series."""
        self.add_object_type_line()
        self.add_index_range_line()
        self.add_dtypes_line()
        if self.display_memory_usage:
            self.add_memory_usage_line()
