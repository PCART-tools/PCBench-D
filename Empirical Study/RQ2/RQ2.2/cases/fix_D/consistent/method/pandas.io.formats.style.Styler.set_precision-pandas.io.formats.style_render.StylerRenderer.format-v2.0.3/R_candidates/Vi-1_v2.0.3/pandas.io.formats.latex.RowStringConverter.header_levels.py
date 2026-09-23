    @property
    def header_levels(self) -> int:
        nlevels = self.column_levels
        if self.fmt.has_index_names and self.fmt.show_index_names:
            nlevels += 1
        return nlevels
