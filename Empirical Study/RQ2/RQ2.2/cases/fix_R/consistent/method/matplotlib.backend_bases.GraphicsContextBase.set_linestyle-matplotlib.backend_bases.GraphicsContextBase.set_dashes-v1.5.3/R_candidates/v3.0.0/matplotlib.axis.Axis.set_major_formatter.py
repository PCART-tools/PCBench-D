    def set_major_formatter(self, formatter):
        """
        Set the formatter of the major ticker.

        Parameters
        ----------
        formatter : ~matplotlib.ticker.Formatter
        """
        if not isinstance(formatter, mticker.Formatter):
            raise TypeError("formatter argument should be instance of "
                    "matplotlib.ticker.Formatter")
        self.isDefault_majfmt = False
        self.major.formatter = formatter
        formatter.set_axis(self)
        self.stale = True
