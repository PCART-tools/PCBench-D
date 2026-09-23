    def format_data_short(self, value):
        """
        Return a short formatted string representation of a number.
        """
        if self._useLocale:
            return locale.format_string('%-12g', (value,))
        else:
            return '%-12g' % value
