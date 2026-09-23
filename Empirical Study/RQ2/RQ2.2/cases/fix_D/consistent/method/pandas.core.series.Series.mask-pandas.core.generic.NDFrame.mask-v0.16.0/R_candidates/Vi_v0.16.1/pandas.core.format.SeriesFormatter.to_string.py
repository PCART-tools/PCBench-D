    def to_string(self):
        series = self.tr_series
        footer = self._get_footer()

        if len(series) == 0:
            return 'Series([], ' + footer + ')'

        fmt_index, have_header = self._get_formatted_index()
        fmt_values = self._get_formatted_values()

        maxlen = max(len(x) for x in fmt_index)  # max index len
        pad_space = min(maxlen, 60)

        if self.truncate_v:
            n_header_rows = 0
            row_num = self.tr_row_num
            width = len(fmt_values[row_num-1])
            if width > 3:
                dot_str = '...'
            else:
                dot_str = '..'
            dot_str = dot_str.center(width)
            fmt_values.insert(row_num + n_header_rows, dot_str)
            fmt_index.insert(row_num + 1, '')

        result = adjoin(3, *[fmt_index[1:], fmt_values])

        if self.header and have_header:
            result = fmt_index[0] + '\n' + result

        if footer:
            result += '\n' + footer

        return compat.text_type(u('').join(result))
