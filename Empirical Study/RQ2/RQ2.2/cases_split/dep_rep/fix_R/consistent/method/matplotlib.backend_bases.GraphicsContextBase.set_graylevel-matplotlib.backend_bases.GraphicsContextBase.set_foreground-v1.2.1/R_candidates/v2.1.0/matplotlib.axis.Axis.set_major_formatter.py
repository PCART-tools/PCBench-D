    def set_major_formatter(self, formatter):
        """
        Set the formatter of the major ticker

        ACCEPTS: A :class:`~matplotlib.ticker.Formatter` instance
        """
        self.isDefault_majfmt = False
        self.major.formatter = formatter
        formatter.set_axis(self)
        self.stale = True
