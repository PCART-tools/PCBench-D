    def set_minor_formatter(self, formatter):
        """
        Set the formatter of the minor ticker.

        Parameters
        ----------
        formatter : ~matplotlib.ticker.Formatter
        """
        if not isinstance(formatter, mticker.Formatter):
            raise TypeError("formatter argument should be instance of "
                    "matplotlib.ticker.Formatter")
        self.isDefault_minfmt = False
        self.minor.formatter = formatter
        formatter.set_axis(self)
        self.stale = True
