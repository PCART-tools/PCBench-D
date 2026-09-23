    def _get_formatted_column_labels(self):
        from pandas.core.index import _sparsify

        def is_numeric_dtype(dtype):
            return issubclass(dtype.type, np.number)

        if self.max_cols:
            columns = self.columns[:self.max_cols]
        else:
            columns = self.columns

        if isinstance(columns, MultiIndex):
            fmt_columns = columns.format(sparsify=False, adjoin=False)
            fmt_columns = lzip(*fmt_columns)
            dtypes = self.frame.dtypes.values
            need_leadsp = dict(zip(fmt_columns, map(is_numeric_dtype, dtypes)))
            str_columns = list(zip(*[
                [' ' + y if y not in self.formatters and need_leadsp[x]
                 else y for y in x] for x in fmt_columns]))
            if self.sparsify:
                str_columns = _sparsify(str_columns)

            str_columns = [list(x) for x in zip(*str_columns)]
        else:
            fmt_columns = columns.format()
            dtypes = self.frame.dtypes
            need_leadsp = dict(zip(fmt_columns, map(is_numeric_dtype, dtypes)))
            str_columns = [[' ' + x
                            if not self._get_formatter(i) and need_leadsp[x]
                            else x]
                           for i, (col, x) in
                           enumerate(zip(columns, fmt_columns))]

        if self.show_index_names and self.has_index_names:
            for x in str_columns:
                x.append('')

        return str_columns
