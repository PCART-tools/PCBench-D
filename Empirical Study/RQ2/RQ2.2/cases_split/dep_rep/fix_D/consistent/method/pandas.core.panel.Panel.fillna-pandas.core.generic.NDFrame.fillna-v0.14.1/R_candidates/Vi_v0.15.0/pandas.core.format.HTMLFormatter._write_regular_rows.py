    def _write_regular_rows(self, fmt_values, indent):
        truncate_h = self.fmt.truncate_h
        truncate_v = self.fmt.truncate_v

        ncols = len(self.fmt.tr_frame.columns)
        nrows = len(self.fmt.tr_frame)
        fmt = self.fmt._get_formatter('__index__')
        if fmt is not None:
            index_values = self.fmt.tr_frame.index.map(fmt)
        else:
            index_values = self.fmt.tr_frame.index.format()

        row = []
        for i in range(nrows):

            if truncate_v and i == (self.fmt.tr_row_num):
                str_sep_row = ['...' for ele in row]
                self.write_tr(str_sep_row, indent, self.indent_delta, tags=None,
                              nindex_levels=1)

            row = []
            row.append(index_values[i])
            row.extend(fmt_values[j][i] for j in range(ncols))

            if truncate_h:
                dot_col_ix = self.fmt.tr_col_num + 1
                row.insert(dot_col_ix, '...')
            self.write_tr(row, indent, self.indent_delta, tags=None,
                          nindex_levels=1)
