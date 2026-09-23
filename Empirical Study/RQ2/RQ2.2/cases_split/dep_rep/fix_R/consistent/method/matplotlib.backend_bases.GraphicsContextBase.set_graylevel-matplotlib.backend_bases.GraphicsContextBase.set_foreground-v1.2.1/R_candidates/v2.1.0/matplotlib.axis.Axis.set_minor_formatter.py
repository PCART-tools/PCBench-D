    def set_minor_formatter(self, formatter):
        """
        Set the formatter of the minor ticker

        ACCEPTS: A :class:`~matplotlib.ticker.Formatter` instance
        """
        self.isDefault_minfmt = False
        self.minor.formatter = formatter
        formatter.set_axis(self)
        self.stale = True
