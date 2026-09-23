    def format_data(self, value):
        # docstring inherited
        if self._useLocale:
            s = locale.format_string('%1.10e', (value,))
        else:
            s = '%1.10e' % value
        s = self._formatSciNotation(s)
        return self.fix_minus(s)
