    def to_string(self):
        series = self.series

        if len(series) == 0:
            return u('')

        fmt_index, have_header = self._get_formatted_index()
        fmt_values = self._get_formatted_values()

        maxlen = max(len(x) for x in fmt_index)
        pad_space = min(maxlen, 60)

        result = ['%s   %s'] * len(fmt_values)
        for i, (k, v) in enumerate(zip(fmt_index[1:], fmt_values)):
            idx = k.ljust(pad_space)
            result[i] = result[i] % (idx, v)

        if self.header and have_header:
            result.insert(0, fmt_index[0])

        footer = self._get_footer()
        if footer:
            result.append(footer)

        return compat.text_type(u('\n').join(result))
