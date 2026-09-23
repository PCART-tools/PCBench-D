    def to_string(self):
        categorical = self.categorical

        if len(categorical) == 0:
            if self.footer:
                return self._get_footer()
            else:
                return u('')

        fmt_values = self._get_formatted_values()
        pad_space = 10

        result = ['%s' % i for i in fmt_values]
        if self.footer:
            footer = self._get_footer()
            if footer:
                result.append(footer)

        return compat.text_type(u('\n').join(result))
