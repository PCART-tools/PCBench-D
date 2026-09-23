    def _to_str_columns(self):
        """
        Render a DataFrame to a list of columns (as lists of strings).
        """

        # may include levels names also
        str_index = self._get_formatted_index()
        str_columns = self._get_formatted_column_labels()

        _strlen = _strlen_func()

        cols_to_show = self.columns[:self.max_cols]
        truncate_h = self.max_cols and (len(self.columns) > self.max_cols)
        truncate_v = self.max_rows and (len(self.frame) > self.max_rows)
        self.truncated_v = truncate_v
        if truncate_h:
            cols_to_show = self.columns[:self.max_cols]
        else:
            cols_to_show = self.columns

        if self.header:
            stringified = []
            for i, c in enumerate(cols_to_show):
                fmt_values = self._format_col(i)
                cheader = str_columns[i]

                max_colwidth = max(self.col_space or 0,
                                   *(_strlen(x) for x in cheader))

                fmt_values = _make_fixed_width(fmt_values, self.justify,
                                               minimum=max_colwidth,
                                               truncated=truncate_v)

                max_len = max(np.max([_strlen(x) for x in fmt_values]),
                              max_colwidth)
                if self.justify == 'left':
                    cheader = [x.ljust(max_len) for x in cheader]
                else:
                    cheader = [x.rjust(max_len) for x in cheader]

                stringified.append(cheader + fmt_values)
        else:
            stringified = [_make_fixed_width(self._format_col(i), self.justify,
                                             truncated=truncate_v)
                           for i, c in enumerate(cols_to_show)]

        strcols = stringified
        if self.index:
            strcols.insert(0, str_index)
        if truncate_h:
            strcols.append(([''] * len(str_columns[-1]))
                           + (['...'] * min(len(self.frame), self.max_rows)))

        return strcols
