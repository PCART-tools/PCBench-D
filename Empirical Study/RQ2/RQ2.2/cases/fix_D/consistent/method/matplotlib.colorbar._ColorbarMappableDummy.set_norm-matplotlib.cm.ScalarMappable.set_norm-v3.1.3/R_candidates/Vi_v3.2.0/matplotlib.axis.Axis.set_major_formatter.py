    def set_major_formatter(self, formatter):
        """
        Set the formatter of the major ticker.

        Parameters
        ----------
        formatter : `~matplotlib.ticker.Formatter`
        """
        cbook._check_isinstance(mticker.Formatter, formatter=formatter)
        self.isDefault_majfmt = False
        self.major.formatter = formatter
        formatter.set_axis(self)
        self.stale = True
