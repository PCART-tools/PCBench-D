    def _format_maybe_minus_and_locale(self, fmt, arg):
        """
        Format *arg* with *fmt*, applying Unicode minus and locale if desired.
        """
        return self.fix_minus(locale.format_string(fmt, (arg,), True)
                              if self._useLocale else fmt % arg)
