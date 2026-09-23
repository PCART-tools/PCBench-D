    def _to_str_columns(self):
        """
        Render a DataFrame to a list of columns (as lists of strings).
        """
        _strlen = _strlen_func()
        frame = self.tr_frame

        # may include levels names also

        str_index = self._get_formatted_index(frame)
        str_columns = self._get_formatted_column_labels(frame)

        if self.header:
            stringified = []
            for i, c in enumerate(frame):
                cheader = str_columns[i]
                max_colwidth = max(self.col_space or 0,
                                   *(_strlen(x) for x in cheader))

                fmt_values = self._format_col(i)

                fmt_values = _make_fixed_width(fmt_values, self.justify,
                                               minimum=max_colwidth)

                max_len = max(np.max([_strlen(x) for x in fmt_values]),
                              max_colwidth)
                if self.justify == 'left':
                    cheader = [x.ljust(max_len) for x in cheader]
                else:
                    cheader = [x.rjust(max_len) for x in cheader]

                stringified.append(cheader + fmt_values)
        else:
            stringified = []
            for i, c in enumerate(frame):
                fmt_values = self._format_col(i)
                fmt_values = _make_fixed_width(fmt_values, self.justify,
                                               minimum=(self.col_space or 0))

                stringified.append(fmt_values)

        strcols = stringified
        if self.index:
            strcols.insert(0, str_index)

        # Add ... to signal truncated
        truncate_h = self.truncate_h
        truncate_v = self.truncate_v

        if truncate_h:
            col_num = self.tr_col_num
            col_width = len(strcols[self.tr_size_col][0])  # infer from column header
            strcols.insert(self.tr_col_num + 1, ['...'.center(col_width)] * (len(str_index)))
        if truncate_v:
            n_header_rows = len(str_index) - len(frame)
            row_num = self.tr_row_num
            for ix, col in enumerate(strcols):
                cwidth = len(strcols[ix][row_num])  # infer from above row
                is_dot_col = False
                if truncate_h:
                    is_dot_col = ix == col_num + 1
                if cwidth > 3 or is_dot_col:
                    my_str = '...'
                else:
                    my_str = '..'

                if ix == 0:
                    dot_str = my_str.ljust(cwidth)
                elif is_dot_col:
                    cwidth = len(strcols[self.tr_size_col][0])
                    dot_str = my_str.center(cwidth)
                else:
                    dot_str = my_str.rjust(cwidth)

                strcols[ix].insert(row_num + n_header_rows, dot_str)
        return strcols
