    def _get_formatted_index(self) -> tuple[list[str], bool]:
        index = self.tr_series.index

        if isinstance(index, MultiIndex):
            have_header = any(name for name in index.names)
            fmt_index = index.format(names=True)
        else:
            have_header = index.name is not None
            fmt_index = index.format(name=True)
        return fmt_index, have_header
