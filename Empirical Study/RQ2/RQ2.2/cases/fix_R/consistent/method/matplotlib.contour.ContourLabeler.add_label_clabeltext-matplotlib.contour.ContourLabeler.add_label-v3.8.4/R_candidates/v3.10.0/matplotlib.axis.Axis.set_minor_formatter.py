    def set_minor_formatter(self, formatter):
        """
        Set the formatter of the minor ticker.

        In addition to a `~matplotlib.ticker.Formatter` instance,
        this also accepts a ``str`` or function.
        See `.Axis.set_major_formatter` for more information.

        Parameters
        ----------
        formatter : `~matplotlib.ticker.Formatter`, ``str``, or function
        """
        self._set_formatter(formatter, self.minor)
