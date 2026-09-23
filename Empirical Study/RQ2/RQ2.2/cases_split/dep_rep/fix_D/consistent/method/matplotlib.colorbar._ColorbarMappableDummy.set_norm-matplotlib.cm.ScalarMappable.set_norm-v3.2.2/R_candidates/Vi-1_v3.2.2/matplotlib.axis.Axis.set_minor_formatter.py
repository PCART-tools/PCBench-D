    def set_minor_formatter(self, formatter):
        """
        Set the formatter of the minor ticker.

        Parameters
        ----------
        formatter : `~matplotlib.ticker.Formatter`
        """
        cbook._check_isinstance(mticker.Formatter, formatter=formatter)
        self.isDefault_minfmt = False
        self.minor.formatter = formatter
        formatter.set_axis(self)
        self.stale = True
