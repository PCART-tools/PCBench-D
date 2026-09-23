    def _write_regular_rows(self, fmt_values, indent, truncated):
        ncols = min(len(self.columns), self.max_cols)
        nrows = min(len(self.frame), self.max_rows)
        fmt = self.fmt._get_formatter('__index__')
        if fmt is not None:
            index_values = self.frame.index[:nrows].map(fmt)
        else:
            index_values = self.frame.index[:nrows].format()

        for i in range(nrows):
            row = []
            row.append(index_values[i])
            row.extend(fmt_values[j][i] for j in range(ncols))
            if truncated:
                row.append('...')
            self.write_tr(row, indent, self.indent_delta, tags=None,
                          nindex_levels=1)

        if len(self.frame) > self.max_rows:
            row = [''] + (['...'] * ncols)
            self.write_tr(row, indent, self.indent_delta, tags=None,
                          nindex_levels=1)
