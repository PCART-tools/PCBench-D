    def to_string(self):
        categorical = self.categorical

        if len(categorical) == 0:
            if self.footer:
                return self._get_footer()
            else:
                return u('')

        fmt_values = self._get_formatted_values()

        result = ['%s' % i for i in fmt_values]
        result = [i.strip() for i in result]
        result = u(', ').join(result)
        result = [u('[')+result+u(']')]
        if self.footer:
            footer = self._get_footer()
            if footer:
                result.append(footer)

        return compat.text_type(u('\n').join(result))
