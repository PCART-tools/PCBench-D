    @formatter.setter
    def formatter(self, formatter):
        if not isinstance(formatter, mticker.Formatter):
            cbook.warn_deprecated(
                "3.2", message="Support for formatters that do not subclass "
                "matplotlib.ticker.Formatter is deprecated since %(since)s "
                "and support for them will be removed %(removal)s.")
        self._formatter = formatter
