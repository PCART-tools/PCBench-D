    def _get_formatted_index(self):
        index = self.series.index
        is_multi = isinstance(index, MultiIndex)

        if is_multi:
            have_header = any(name for name in index.names)
            fmt_index = index.format(names=True)
        else:
            have_header = index.name is not None
            fmt_index = index.format(name=True)
        return fmt_index, have_header
